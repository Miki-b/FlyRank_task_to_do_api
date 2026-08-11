from dotenv import load_dotenv 
import psycopg 
import os
from fastapi import HTTPException
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

async def get_all_tasks():
    try:
        cursor.execute("select * from tasks")
        rows = cursor.fetchall()
        return [{"id":r[0],"title":r[1],"done":r[2] } for r in rows ]
    except Exception as e:
        raise HTTPException(status_code=400,detail="Unable to read {e}")

async def get_tasks_by_id(id:int):
    try:
        
        
        cursor.execute("SELECT * FROM tasks WHERE id = $s",(id,))
        
        row = cursor.fetchone()
        
        print(row)
        if row is None:
            raise HTTPException(status_code=404,detail="Record is not available")
        return [{"id":row[0],"title":row[1],"done":row[2]}]
    except Exception as e:
          raise HTTPException(status_code=400,detail="Unable to read one record {e}")
    
async def post_tasks(title: str):
    if title is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "title is empty"
        )
    elif not isinstance(title, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "title must be text"
        )
    else:
        try:
            cursor.execute(" Insert into tasks(title) values(?)",(title,))
            db.commit()
            return {"message":"Task saved successfully...!"}
        except Exception as e:
            raise HTTPException(status_code=400,detail="Unable to store {e}")
        

async def update_task(id: int, task:Task):
    if task.title is None or task.done is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "title or done is empty"
        )
    elif type(task.title) != str or type(task.done) != bool:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "title must be text and done must be boolean"
            )
    
    try:
        cursor.execute("update tasks set title=?,done=? where id=?",(task.title,task.done, id))
        db.commit()
        return {"Message": "Task updated successfully..."}
    except Exception as e:
          raise HTTPException(status_code=400,detail="Unable to update record {e}")

async def delete_task(id: int):
    try:
        cursor.execute("Delete from tasks where id=?",(id,))
        db.commit()
        return {"Message": "task deleted successfully..."}
    except Exception as e:
          raise HTTPException(status_code=400,detail="Unable to delete record {e}")
            
    