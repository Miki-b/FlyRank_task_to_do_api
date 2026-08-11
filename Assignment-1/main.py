from fastapi import FastAPI,  HTTPException, status
from pydantic import BaseModel
import database

app = FastAPI()


class Task(BaseModel):
    title: str
    done: bool



@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")

async def get_all_tasks():
    return database.get_all_tasks()



@app.get("/tasks/{id}")
async def get_tasks_by_id(id:int):
    return database.get_tasks_by_id(id)
    
    
@app.post("/tasks", status_code = 201)
async def post_tasks(title: str):
    return database.post_tasks(title)
    
@app.put("/tasks/{id}", status_code = 201)
async def update_task(id: int, task:Task):
    return database.update_task(id, task)

@app.delete("/tasks/{id}", status_code = 204)
async def delete_task(id: int):
    return database.delete_task(id)
