from fastapi import FastAPI

import database
from models import Task


app = FastAPI()


@app.get("/")
async def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


@app.get("/tasks")
async def get_all_tasks():
    return await database.get_all_tasks()


@app.get("/tasks/{id}")
async def get_tasks_by_id(id: int):
    return await database.get_tasks_by_id(id)


@app.post("/tasks", status_code=201)
async def post_tasks(task: Task):
    return await database.post_tasks(
        task.title,
        task.done
    )


@app.put("/tasks/{id}")
async def update_task(id: int, task: Task):
    return await database.update_task(id, task)


@app.delete("/tasks/{id}")
async def delete_task(id: int):
    return await database.delete_task(id)