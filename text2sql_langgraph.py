import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode
from sqlalchemy import create_engine
# Database tools (copied from notebook)
from typing import List
from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig
from sqlalchemy import text
import sqlalchemy

@tool
def list_tables_tool(config: RunnableConfig) -> List[str]:
    """List all tables in database"""
    db_engine = config.get("configurable", {}).get("db_engine")
    inspector = sqlalchemy.inspect(db_engine)
    return inspector.get_table_names()

@tool
def get_table_schema_tool(table_name: str, config: RunnableConfig) -> List[dict]:
    """Get schema information about a table"""
    db_engine = config.get("configurable", {}).get("db_engine")
    inspector = sqlalchemy.inspect(db_engine)
    return inspector.get_columns(table_name)

@tool
def execute_sql_tool(query: str, config: RunnableConfig) -> List[tuple]:
    """Execute SQL query and return results"""
    db_engine = config.get("configurable", {}).get("db_engine")
    with db_engine.begin() as connection:
        result = connection.execute(text(query)).fetchall()
    return result
from dotenv import load_dotenv

load_dotenv()

class State(MessagesState):
    user_query: str

def create_text2sql_agent():
    dba_tools = [list_tables_tool, get_table_schema_tool, execute_sql_tool]
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.0)
    dba_llm = llm.bind_tools(dba_tools, tool_choice="auto")
    workflow = StateGraph(State)
    
    def messages_builder(state: State):
        dba_sys_msg = (
            "You are an expert SQL developer. Use the available tools to understand the database structure and generate accurate SQL queries.\n\n"
            "Available tools:\n"
            "- list_tables_tool: See what tables exist\n"
            "- get_table_schema_tool: Understand table structure\n"
            "- execute_sql_tool: Run your SQL query\n\n"
            "Generate valid SQL for the given database and provide clear results."
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
    
    react_graph = workflow.compile()
    return react_graph

#===============================================================================
#===============================================================================
def main():
    st.title("Text2SQL LangGraph")
    st.write("Ask questions about the Sakila database using AI agents!")
    
    if 'agent' not in st.session_state:
        st.session_state.agent = create_text2sql_agent()
    
    if 'db_engine' not in st.session_state:
        st.session_state.db_engine = create_engine("sqlite:///data/sakila_master.db")
    
    user_query = st.text_area("Enter your question about the database:", height=100)
    
    if st.button("Submit Query") and user_query:
        with st.spinner("Processing your query..."):
            try:
                config = {'configurable': {'db_engine': st.session_state.db_engine}, 'recursion_limit': 25}
                inputs = {'user_query': user_query}
                
                messages = st.session_state.agent.invoke(input=inputs, config=config)
                
                # Show SQL query
                for message in messages['messages']:
                    if hasattr(message, 'tool_calls') and message.tool_calls:
                        for tool_call in message.tool_calls:
                            if tool_call['name'] == 'execute_sql_tool':
                                st.code(tool_call['args']['query'], language='sql')
                                break
                
                # Show result
                final_response = messages['messages'][-1].content
                st.write(final_response)
                
                with st.expander("View conversation details"):
                    for i, message in enumerate(messages['messages']):
                        if hasattr(message, 'content') and message.content:
                            if i == 0:
                                st.write("**System Message:**", message.content)
                            elif i == 1:
                                st.write("**Your Question:**", message.content)
                            else:
                                st.write(f"**Message {i}:**", message.content)
                        
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
if __name__ == "__main__":
    main()