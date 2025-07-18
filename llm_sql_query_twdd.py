import pyodbc
from sqlalchemy import create_engine, inspect, URL
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.ollama import Ollama
import time

# MSSQL connection settings
server = "ZELIS\\REEDUS"
database = "TWD_Database"
username = "sa"
password = "daryldixon"
driver = "ODBC Driver 17 for SQL Server"
schema = "dbo"

# SQLAlchemy connection URL
connection_url = URL.create(
    "mssql+pyodbc",
    username=username,
    password=password,
    host=server,
    database=database,
    query={"driver": driver}
)

# Create engine
engine = create_engine(connection_url)

# Check available tables
inspector = inspect(engine)
available_tables = inspector.get_table_names(schema=schema)
print(f"Available tables: {available_tables}")

# Check for required tables
required_tables = {"characters", "appearances"}
missing_tables = required_tables - set(available_tables)
if missing_tables:
    print(f"Warning: Missing tables - {missing_tables}")

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
    system_prompt=(
        "You are a SQL expert for The Walking Dead database. "
        "Use these tables/columns:\n"
        "- characters: id, name, status, species, gender\n"
        "- appearances: id, character_id, episode, season\n\n"
        "Rules:\n"
        "1. Use exact column/table names\n"
        "2. Use explicit JOIN syntax\n"
        "3. Handle NULL values\n"
        "4. Use aliases when needed\n"
        "5. Convert questions to precise SQL"
    )
)

# Create query engine
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=list(required_tables),
    llm=llm
)

print("\nSystem ready. Ask about The Walking Dead characters and appearances.")
print("Type 'exit' to quit.\n")

while True:
    try:
        user_query = input("\nYour query: ").strip()
        if user_query.lower() == 'exit':
            break

        start_time = time.time()
        response = query_engine.query(user_query)
        exec_time = time.time() - start_time

        print(f"\nResponse ({exec_time:.2f}s):")
        print(str(response).strip())

        # Access SQL query from response
        if hasattr(response, 'metadata') and 'sql_query' in response.metadata:
            print(f"\nGenerated SQL: {response.metadata['sql_query']}")
        else:
            print("\nNo SQL metadata found in response")

    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please try a different question format\n")

print("Exiting...")