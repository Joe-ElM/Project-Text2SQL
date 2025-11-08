from sqlalchemy import create_engine

def get_engine(db_type: str = "sqlite", dsn: str = None):
    """Factory function to create database engine"""
    if dsn:
        return create_engine(dsn)
    
    # Default DSNs for each database type
    if db_type == "sqlite":
        return create_engine("sqlite:///data/sakila_master.db")
    elif db_type == "postgresql":
        return create_engine("postgresql://user:password@localhost/database")
    elif db_type == "mysql":
        return create_engine("mysql://user:password@localhost/database")
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

def get_connection(db_type: str = "sqlite", dsn: str = None):
    """Factory function to create database connection"""
    engine = get_engine(db_type, dsn)
    return engine.connect()