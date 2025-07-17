import pyodbc
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL
from llama_index.core import SQLDatabase
from llama_index.llms.ollama import Ollama
from llama_index.core.query_engine import NLSQLTableQueryEngine
import time

# MSSQL connection settings
server = "ZELIS\\REEDUS"
database = "walking_dead_db"
username = "sa"
password = "daryldixon"
driver = "ODBC Driver 17 for SQL Server"
schema = "dbo"

# SQLAlchemy connection string
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
connection_url = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": connection_string}
)

# Create engine
engine = create_engine(connection_url)

# Check available tables
inspector = inspect(engine)
available_tables = inspector.get_table_names(schema=schema)

# Check for required tables
required_tables = {"characters", "appearances"}
missing_tables = required_tables - set(available_tables)
if missing_tables:
    raise ValueError(f"Missing tables: {missing_tables}\nAvailable tables: {available_tables}")

# SQLDatabase wrapper
sql_database = SQLDatabase(
    engine,
    include_tables=list(required_tables),
    schema=schema
)

# Configure Ollama LLM
llm = Ollama(
    model="gemma:2b",
    request_timeout=300.0,
    num_gpu=0,
    num_thread=2,
    system_prompt = (
    "You are a SQL expert. Only use the tables 'characters' and 'appearances' when generating SQL queries. "
    "Use the exact column names and table names as they exist in the database. "
    "Do not guess or invent table or column names. Your task is to translate natural language questions into accurate SQL queries."
)

)

# Create query engine
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=list(required_tables),
    llm=llm,
    embed_model="local",
    synthesize_response=True
)


while True:
    try:
        user_query = input("\nYour query: ")

        if user_query.lower() == 'exit':
            break

        start_time = time.time()
        response = query_engine.query(user_query)
        exec_time = time.time() - start_time

        print(f"\nResponse ({exec_time:.2f}s):")
        print(str(response).strip())

        if hasattr(response, 'metadata') and 'sql_query' in response.metadata:
            print(f"\nGenerated SQL: {response.metadata['sql_query']}")

    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please rephrase your query or check the table names.\n")

print("Exiting...")
