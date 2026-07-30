from fastapi import FastAPI,  HTTPException, status
from pydantic import BaseModel
import sqlite3

app = FastAPI()
db = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = db.cursor()

class Task(BaseModel):
    title: str
    done: bool

cursor.execute(''' 
            create table if not exists tasks(
               id integer primary key autoincrement,
               title text not null,
               done boolean
               )
            ''')
cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]


if count == 0:
    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        [
            ("Learn SQLite", 0),
            ("Build a Todo API", 0),
            ("Submit assignment", 1),
        ],
    )
    print("Example tasks inserted.")
else:
    print("Database already contains data.")




db.commit()
   


@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")
async def get_all_tasks():
    try:
        cursor.execute("select * from tasks")
        rows = cursor.fetchall()
        return [{"id":r[0],"title":r[1],"done":r[2] } for r in rows ]
    except Exception as e:
        return HTTPException(status_code=400,detail="Unable to read {e}")



@app.get("/tasks/{id}")
async def get_tasks_by_id(id:int):
    try:
        cursor.execute("select * from tasks where id = ?",(id))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404,detail="Record is not available")
        return [{"id":row[0],"title":row[1],"done":row[2]}]
    except Exception as e:
          return HTTPException(status_code=400,detail="Unable to read one record {e}")
    
    
@app.post("/tasks", status_code = 201)
async def post_tasks(title: str):
    
    if title is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "title is empty"
        )
    elif title is not str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "title must be text"
        )
    else:
        try:
            cursor.execute(" Insert into tasks(title) values(?,?)",(title))
            db.commit()
            return {"message":"Task saved successfully...!"}
        except Exception as e:
            return HTTPException(status_code=400,detail="Unable to store {e}")

@app.put("/tasks/{id}", status_code = 201)
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
        cursor.execute("update tasks set title=?,done=? where id=?",(id,task.title,task.done))
        db.commit()
        return {"Message": "Task updated successfully..."}
    except Exception as e:
          return HTTPException(status_code=400,detail="Unable to update record {e}")


@app.delete("/tasks/{id}", status_code = 204)
async def delete_task(id: int):
    try:
        cursor.execute("Delete from items where item_id=?",(id))
        db.commit()
        return {"Message": "Item deleted successfully..."}
    except Exception as e:
          return HTTPException(status_code=400,detail="Unable to delete record {e}")
            
    
