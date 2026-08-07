from dotenv import load_dotenv 
import psycopg 
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg.connect(DATABASE_URL)
conn.autocommit = True

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL
)
""")

cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (%s, %s)",
        [
            ("Learn PostgreSQL", False),
            ("Build a Todo API", False),
            ("Submit assignment", True),
        ],
    )