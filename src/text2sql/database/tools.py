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