import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.text2sql.agents.text2sql_agent import create_text2sql_agent
from src.text2sql.database.factory import get_engine
from src.text2sql.config import DB_TYPE


def main():
    # Fixed input at top
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    
    user_query = st.text_area("Enter your question:", height=100, placeholder="Ask about your database...", key=f"input_{st.session_state.input_key}")
    submit_clicked = st.button("Submit Query")
    
    # Sidebar
    with st.sidebar:
        st.title("Text2SQL Agent")
        st.header("🔑 API Key")
        user_api_key = st.text_input("OpenAI API Key (required):", type="password", placeholder="Enter your OpenAI API key")
        
        st.header("🤖 Model")
        model_options = ["GPT-4o", "GPT-4o-mini"]
        selected_model = st.selectbox("Model:", model_options)
        
        st.header("🗄️ Database")
        
        # Database type selector
        db_options = ["SQLite", "PostgreSQL", "MySQL"]
        db_type = st.selectbox("Type:", db_options).lower()
        
        # Connection input
        if db_type == "sqlite":
            uploaded_file = st.file_uploader("Upload SQLite file:", type=['db', 'sqlite'])
            if uploaded_file:
                # Save uploaded file temporarily
                with open("temp_db.db", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                custom_dsn = "sqlite:///temp_db.db"
            else:
                custom_dsn = None
        else:
            connection_string = st.text_input("Connection String:", placeholder="postgresql://user:pass@host/db")
            
            # Schema selector for PostgreSQL
            if db_type == "postgresql" and connection_string:
                schema_name = st.text_input("Schema (optional):", placeholder="public")
                if schema_name:
                    # Add schema to connection string
                    custom_dsn = f"{connection_string}?options=-csearch_path={schema_name}"
                else:
                    custom_dsn = connection_string
            else:
                custom_dsn = connection_string if connection_string else None
        
        # Connection status
        if custom_dsn:
            st.success(f"✅ Using custom connection")
        else:
            st.info(f"ℹ️ Using default {db_type} database")
    
    # Use default database type
    selected_db = db_type.title()
    
    # Set API key
    if user_api_key:
        import os
        os.environ["OPENAI_API_KEY"] = user_api_key
    
    # Show API key requirement
    if not user_api_key:
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar to use the Text2SQL Agent.")
        st.stop()
    
    # Create agent and engine
    if 'agent' not in st.session_state or st.session_state.get('db_type') != db_type or st.session_state.get('api_key') != user_api_key or st.session_state.get('model') != selected_model:
        st.session_state.agent = create_text2sql_agent(db_type, selected_model.lower())
        st.session_state.db_type = db_type
        st.session_state.api_key = user_api_key
        st.session_state.model = selected_model
    
    if 'db_engine' not in st.session_state or st.session_state.get('db_type') != db_type or st.session_state.get('custom_dsn') != custom_dsn:
        if custom_dsn:
            from sqlalchemy import create_engine
            st.session_state.db_engine = create_engine(custom_dsn)
        else:
            st.session_state.db_engine = get_engine(db_type)
        st.session_state.custom_dsn = custom_dsn
    
    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history (newest first)
    for chat in reversed(st.session_state.chat_history):
        st.write(f"🟡 **You:** {chat['query']}")
        if chat.get('sql'):
            st.code(chat['sql'], language='sql')
        st.write(f"🔴 **AI:** {chat['response']}")
        st.divider()
    
    if submit_clicked and user_query:
        with st.spinner("Processing your query..."):
            try:
                config = {'configurable': {'db_engine': st.session_state.db_engine, 'thread_id': 'user_session'}, 'recursion_limit': 25}
                inputs = {'user_query': user_query}
                
                messages = st.session_state.agent.invoke(input=inputs, config=config)
                
                # Show SQL query
                sql_query = None
                for message in messages['messages']:
                    if hasattr(message, 'tool_calls') and message.tool_calls:
                        for tool_call in message.tool_calls:
                            if tool_call['name'] == 'execute_sql_tool':
                                sql_query = tool_call['args']['query']
                                st.code(sql_query, language='sql')
                                break
                
                # Show result
                final_response = messages['messages'][-1].content
                st.write(final_response)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    'query': user_query,
                    'response': final_response,
                    'sql': sql_query
                })
                
                # Clear input for next query
                st.session_state.input_key += 1
                st.rerun()
                
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