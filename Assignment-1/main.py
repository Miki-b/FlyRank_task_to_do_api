from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    isDone: bool

Tasks: list[Task] = [{ "ID": 1, "Title" : "get up", "Done": True},{ "ID": 2, "Title" : "get up", "Done": True},{ "ID": 3, "Title" : "get up", "Done": True} ]


@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def root():
    return { "status": "ok" }

@app.get("/tasks")
async def root():
    return Tasks


@app.get("/tasks/{id}")
async def root(id:int):
    for task in Tasks:
        if task["ID"] == id:
            return task
    return { "error": f"Task {id} not found" }
    
    
