from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: generate sample data
    print("Generating sample data...")
    generate_sample_data()
    yield
    # Shutdown code: no action needed
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# In-memory database (for simplicity)
todos = []

class Todo(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class ToDoInDB(Todo):
    id: UUID    

def generate_sample_data():
    todos.append(ToDoInDB(id=uuid4(), title="Learn FastAPI", description="Need to learn FastAPI to build APIs quickly"))
    todos.append(ToDoInDB(id=uuid4(), title="Build an API", description="Need to build an API using FastAPI"))
    todos.append(ToDoInDB(id=uuid4(), title="Deploy the API", description="Need to deploy the API on the cloud"))

@app.get("/todos", response_model=List[ToDoInDB])
def get_todos():
    return todos

@app.get("/todos/{todo_id}", response_model=ToDoInDB)
def get_todo_by_id(todo_id: UUID):
    print(todo_id)
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos", response_model=ToDoInDB, status_code=201)
def create_todo(todo: Todo):
    new_todo = ToDoInDB(id=uuid4(), **todo.model_dump())
    todos.append(new_todo)
    return new_todo 