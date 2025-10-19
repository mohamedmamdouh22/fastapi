from fastapi import FastAPI
from models import Base
from database import engine

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def read_all():
    return {"Hello": "World"}
