import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

conn = psycopg.connect(
    dbname="expense_tracker",
    user="postgres",
    password=os.getenv("PG_PASSWORD"),
    host="localhost",
    port=5432
)

print("Connected to PostgreSQL!")

conn.close()