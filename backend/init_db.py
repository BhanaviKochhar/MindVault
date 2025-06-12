import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def init_db():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()

    with open("schema.sql", "r") as f:
        cur.execute(f.read())

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database initialized successfully.")

if __name__ == "__main__":
    init_db()
