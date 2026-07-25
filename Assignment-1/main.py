from fastapi import FastAPI,  HTTPException, status
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
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Task {id} not found"
        )
    
@app.post("/tasks")
async def root(title: str):
    if title is not None:
        
    elif title is None:
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
        new_task = Task(id=len(Tasks)+1, title=title, isDone=False)
        Tasks.append(new_task)
        return {"done, here's your receipt"}
    