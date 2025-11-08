import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_DSN = os.getenv("DB_DSN", "sqlite:///data/sakila_master.db")

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")