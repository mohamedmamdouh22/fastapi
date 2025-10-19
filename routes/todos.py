from database import SessionLocal
from models import Todos
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, status


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_session = Depends(get_db)


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_allTodos(db: Session = db_session):
    todos = db.query(Todos).all()
    return todos
