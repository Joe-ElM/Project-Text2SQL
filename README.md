# Text2SQL Agent

A professional AI-powered application that converts natural language questions into SQL queries and executes them against your database. Built with LangGraph, Streamlit, and OpenAI's GPT models.

![Text2SQL Agent Demo](https://img.shields.io/badge/Status-Live%20Deployment-success)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://text2sql-project.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

🔗 **[Try the Live Demo](https://text2sql-project.streamlit.app/)** - Transform your questions into SQL queries instantly!

> **Note**: You'll need your own OpenAI API key to use the application. This ensures data privacy and cost control.

## Features

### Core Functionality

- **Natural Language to SQL**: Convert questions into optimized SQL queries
- **Multi-Database Support**: SQLite, PostgreSQL, MySQL with schema selection
- **AI-Powered Analysis**: GPT-4o and GPT-4o-mini model selection
- **Memory & Context**: Conversational interface with chat history
- **Real-time Execution**: Execute queries and display results instantly

### User Experience

- **Clean UI**: Professional Streamlit interface with sidebar controls
- **API Key Required**: Users provide their own OpenAI key for privacy and cost control
- **Database Upload**: Upload SQLite files or connect via connection strings
- **SQL Display**: View generated SQL queries alongside natural language responses
- **Chat History**: Persistent conversation with visual icons

### Technical Features

- **LangGraph Workflow**: Structured agent with tool integration
- **Database Agnostic Tools**: SQLAlchemy-based tools work across all databases
- **Memory Management**: Built-in conversation memory with checkpointing
- **Error Handling**: Comprehensive error management and user feedback

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (optional - app provides fallback)

### Local Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Joe-ElM/Project-Text2SQL-.git
   cd Project-Text2SQL-
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys (optional)
   ```

4. **Run the application**
   ```bash
   streamlit run app/app.py
   ```

## Configuration

### Environment Variables (.env)

```bash
OPENAI_API_KEY=your_openai_api_key_here
DB_TYPE=sqlite
DB_DSN=sqlite:///data/sakila_master.db
```

### Supported Models

- **GPT-4o**: Best performance, higher cost
- **GPT-4o-mini**: Balanced performance and cost

### Database Support

- **SQLite**: File upload or local files
- **PostgreSQL**: Connection string with optional schema selection
- **MySQL**: Connection string support

## Usage

### Quick Start

1. Open the application in your browser
2. Select your preferred AI model in the sidebar
3. Choose database type and upload/connect your database
4. Ask natural language questions about your data

### Example Queries

```
"Show me all customers from California"
"What are the top 5 best-selling products?"
"Find customers who haven't made a purchase in the last 30 days"
"Show revenue by month for the last year"
```

### Database Connection Examples

**SQLite (File Upload)**

- Use the file uploader in the sidebar
- Supports .db and .sqlite files

**PostgreSQL**

```
postgresql://username:password@localhost:5432/database_name
```

**PostgreSQL with Schema**

```
Connection: postgresql://username:password@localhost:5432/database_name
Schema: public
```

**MySQL**

```
mysql://username:password@localhost:3306/database_name
```

## Architecture

### Project Structure

```
├── app/
│   └── app.py                 # Streamlit UI application
├── src/
│   └── text2sql/
│       ├── agents/
│       │   └── text2sql_agent.py    # LangGraph agent implementation
│       ├── database/
│       │   ├── factory.py           # Database engine factory
│       │   └── tools.py             # Database interaction tools
│       ├── core/
│       │   └── query_engine.py      # Core query processing (placeholder)
│       ├── utils/
│       │   └── helpers.py           # Utility functions
│       └── config.py                # Configuration management
├── data/
│   └── sakila_master.db            # Sample SQLite database
├── tests/
│   └── test_smoke.py               # Basic tests
├── requirements.txt                # Python dependencies
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
└── CLAUDE.md                      # Development notes
```

### Key Components

**LangGraph Agent** (`src/text2sql/agents/text2sql_agent.py`)

- Workflow-based SQL generation
- Tool integration for database operations
- Memory management with checkpointing

**Database Tools** (`src/text2sql/database/tools.py`)

- `list_tables_tool`: Discover available tables
- `get_table_schema_tool`: Inspect table structures
- `execute_sql_tool`: Execute generated queries

**Streamlit UI** (`app/app.py`)

- Clean, professional interface
- Sidebar controls for configuration
- Chat-style conversation history

## Deployment

### Streamlit Cloud

1. Push to GitHub repository
2. Connect repository to Streamlit Cloud
3. Set environment variables in Streamlit Cloud dashboard
4. Deploy automatically

### Railway/Render

1. Connect GitHub repository
2. Configure build command: `pip install -r requirements.txt`
3. Configure start command: `streamlit run app/app.py --server.port=$PORT`
4. Set environment variables
5. Deploy

### Docker (Optional)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app/app.py", "--server.port=8501"]
```

## Security & Privacy

### Enterprise Considerations

- **Data Privacy**: No data stored permanently, only session-based memory
- **API Key Security**: Users can provide their own OpenAI keys
- **Database Security**: Supports read-only operations by default
- **Local Deployment**: Can be deployed on-premises for sensitive data

### For Production Use

- Consider self-hosted LLM models for complete data privacy
- Implement user authentication for multi-user environments
- Add audit logging for compliance requirements
- Use Azure OpenAI for enterprise-grade security

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **LangChain/LangGraph**: For the agent framework
- **OpenAI**: For GPT models
- **Streamlit**: For the web interface
- **SQLAlchemy**: For database abstraction
