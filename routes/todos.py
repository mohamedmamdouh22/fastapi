from typing import Annotated
from database import SessionLocal
from models import Todos
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status, HTTPException, Path
from pydantic import BaseModel, Field

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_session = Depends(get_db)


class Todo(BaseModel):
    title: str = Field(..., min_length=3)
    description: str | None = Field(default=None)
    priority: int = Field(..., ge=1, le=5)
    complete: bool = Field(default=False)


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_allTodos(db: Session = db_session):
    todos = db.query(Todos).all()
    return todos


@router.get("/todos/{todo_id}")
async def read_todo(todo_id: Annotated[int, Path(gt=0)], db: Session = db_session):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: Todo, db: Session = db_session):
    todo = Todos(**todo.model_dump())
    db.add(todo)
    db.commit()
    return todo