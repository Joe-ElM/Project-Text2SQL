from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from src.text2sql.database.tools import list_tables_tool, get_table_schema_tool, execute_sql_tool
from dotenv import load_dotenv

load_dotenv()

class State(MessagesState):
    user_query: str

def create_text2sql_agent(db_type="sqlite", model="gpt-4o"):
    dba_tools = [list_tables_tool, get_table_schema_tool, execute_sql_tool]
    llm = ChatOpenAI(model=model, temperature=0.0)
    dba_llm = llm.bind_tools(dba_tools, tool_choice="auto")
    workflow = StateGraph(State)
    
    def messages_builder(state: State):
        dialect = db_type.upper()
        dba_sys_msg = (
            f"You are an expert database analyst and SQL developer. Convert natural-language questions into accurate {dialect} SQL with clear explanations.\n\n"
            "WORKFLOW:\n"
            "1. Use list_tables_tool to discover available tables\n"
            "2. Use get_table_schema_tool for relevant tables (columns, types, keys)\n"
            "3. Infer table relationships from foreign keys and column names if joins needed\n"
            f"4. Generate SELECT-only query in {dialect} syntax:\n"
            "   • Add LIMIT 50 unless user specifies otherwise\n"
            "   • Use explicit column lists over SELECT *\n"
            "   • Always provide meaningful column aliases using AS keyword\n"
            "   • Apply appropriate JOINs, filters, and aggregations\n"
            "5. Execute query using execute_sql_tool\n"
            "6. Summarize results in plain English\n\n"
            "CONSTRAINTS:\n"
            "• READ-ONLY: Never INSERT/UPDATE/DELETE/DDL operations\n"
            "• Always inspect schema before writing SQL\n"
            f"• Use {dialect} syntax only - no mixing database dialects\n"
            "• Handle impossible requests: explain limitations and suggest alternatives\n"
            "• Provide meaningful column aliases for clarity\n\n"
            "Generate accurate, safe SQL that answers the user's question completely."
        )
        
        messages = [
            SystemMessage(dba_sys_msg),
            HumanMessage(state['user_query'])
        ]
        
        return {'messages': messages}
    
    def dba_agent(state: State):
        ai_message = dba_llm.invoke(state['messages'])
        ai_message.name = "dba_agent"
        return {'messages': ai_message}
    
    def should_continue(state: State):
        last_message = state['messages'][-1]
        if last_message.tool_calls:
            return 'dba_tools'
        return END
    
    
    workflow.add_node("messages_builder", messages_builder)
    workflow.add_node("dba_agent", dba_agent)
    workflow.add_node("dba_tools", ToolNode(dba_tools))
    
    workflow.add_edge(START, "messages_builder")
    workflow.add_edge("messages_builder", "dba_agent")
    workflow.add_conditional_edges(
        source="dba_agent", 
        path=should_continue, 
        path_map=["dba_tools", END]
    )
    workflow.add_edge("dba_tools", "dba_agent")
    
    memory = MemorySaver()
    react_graph = workflow.compile(checkpointer=memory)
    return react_graph
