from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List

app = FastAPI()

# In-memory database (for simplicity)
todos = []

class Todo(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class ToDoInDB(Todo):
    id: UUID    

@app.get("/todos/", response_model=List[ToDoInDB])
def get_todos():
    todo1 = ToDoInDB(id=uuid4(), title="Buy milk", description="Buy 2 gallons of milk")
    todo2 = ToDoInDB(id=uuid4(), title="Pick up kids", description="Pick up kids from school")
    todos.append(todo1)
    todos.append(todo2)
    return todos