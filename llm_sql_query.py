import pyodbc
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL
from llama_index.core import SQLDatabase
from llama_index.llms.ollama import Ollama
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.indices.struct_store.sql_query import NLSQLTableQueryEngine
import time

# MSSQL bağlantı ayarları
server = "ZELIS\\REEDUS"
database = "MyDatabase"
username = "sa"
password = "daryldixon"
driver = "ODBC Driver 17 for SQL Server"
schema = "dbo"  # Genelde varsayılan şema budur

# SQLAlchemy engine oluştur
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
connection_url = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": connection_string}
)
engine = create_engine(connection_url)

# Bağlantıdan tabloları kontrol et
inspector = inspect(engine)
available_tables = inspector.get_table_names(schema=schema)

if "documents" not in available_tables:
    raise ValueError(f"'documents' tablosu '{schema}' şemasında bulunamadı.\nMevcut tablolar: {available_tables}")

# SQLDatabase wrapper oluştur
sql_database = SQLDatabase(
    engine,
    include_tables=["documents"],
    schema=schema
)

# Ollama LLM ayarları
llm = Ollama(
    model="gemma:2b",
    request_timeout=300.0,
    num_gpu=0,
    num_thread=2,
    system_prompt="Sen Türkçe konuşan bir SQL uzmanısın. Kullanıcıların doğal dildeki Türkçe sorgularını SQL'e çevirirken Türkçe karakterlere dikkat etmelisin."
)

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["documents"],
    llm=llm,
    embed_model="local",  # 🔧 Bu satır önemli!
    synthesize_response=True
)

# Etkileşimli sohbet döngüsü
print("SQL veritabanıyla Türkçe sohbet başlatıldı! (Çıkmak için 'exit' yazın)")

while True:
    try:
        user_query = input("\nSorgunuz: ")

        if user_query.lower() == 'exit':
            break

        start_time = time.time()
        response = query_engine.query(user_query)
        exec_time = time.time() - start_time

        print(f"\nYanıt ({exec_time:.2f}s):")
        print(str(response).strip())
        print("\n" + "-" * 50)

        if hasattr(response, 'metadata') and 'sql_query' in response.metadata:
            print(f"\nOluşturulan SQL: {response.metadata['sql_query']}")

    except Exception as e:
        print(f"\nHata oluştu: {str(e)}")
        print("Lütfen sorgunuzu yeniden ifade edin veya tablo adını kontrol edin.\n")

print("\nÇıkış yapılıyor...")
