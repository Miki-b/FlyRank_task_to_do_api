from fastapi import FastAPI,  HTTPException, status
from pydantic import BaseModel
app = FastAPI()

class Task(BaseModel):
    def  __init__(self, id, title, isDone):
        self.id:int = id
        self.title:str= title
        self.isDone:bool = isDone

Tasks: list[Task] = [ 
    Task ( 1,  "get up", True),
    Task ( 2,  "brush teeth", True),
    Task ( 3,  "eat breakfast", True),
    Task ( 4,  "go to work", False),]


@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")
async def get_all_tasks():
    return Tasks


@app.get("/tasks/{id}")
async def get_tasks_by_id(id:int):
    for task in Tasks:
        if task.id == id:
            return task
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Task {id} not found"
        )
    
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
        new_task = Task(id=len(Tasks)+1, title=title, isDone=False)
        Tasks.append(new_task)
        return {"done, here's your receipt"}


@app.put("/tasks/{id}", status_code = 201)
async def update_task(id: int, title: str ,done: bool):
    if title is None or done is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "title or done is empty"
        )
    elif type(title) != str or type(done) != bool:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "title must be text and done must be boolean"
            )
    
    for task in Tasks:
        if task.id == id :
            task.title = title
            task.isDone = done
            return task
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail= f"Task {id} not found"
        )


@app.delete("/tasks/{id}", status_code = 204)
async def delete_task(id: int):
    for task in Tasks:
        if task.id == id :
            Tasks.remove(task)
            return {"No Content"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail= f"Task {id} not found"
        )
        
            
    
