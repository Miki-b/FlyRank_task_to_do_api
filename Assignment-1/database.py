from dotenv import load_dotenv
import psycopg
import os
from fastapi import HTTPException

from models import Task

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

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
        ]
    )


async def get_all_tasks():
    try:
        cursor.execute("SELECT * FROM tasks")

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "done": row[2]
            }
            for row in rows
        ]

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to read: {e}"
        )


async def get_tasks_by_id(id: int):
    try:
        cursor.execute(
            "SELECT * FROM tasks WHERE id = %s",
            (id,)
        )

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Record is not available"
            )

        return {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to read one record: {e}"
        )


async def post_tasks(title: str, done: bool):
    try:
        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            RETURNING *
            """,
            (title, done)
        )

        row = cursor.fetchone()

        return {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to store: {e}"
        )


async def update_task(id: int, task: Task):
    try:
        cursor.execute(
            """
            UPDATE tasks
            SET title = %s, done = %s
            WHERE id = %s
            RETURNING *
            """,
            (task.title, task.done, id)
        )

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to update record: {e}"
        )


async def delete_task(id: int):
    try:
        cursor.execute(
            "DELETE FROM tasks WHERE id = %s RETURNING id",
            (id,)
        )

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return {
            "message": "Task deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to delete record: {e}"
        )