from fastapi import FastAPI
from enum import Enum
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def get():
    return {"message": "Fuck Fe Fe"}


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


@app.get("/user/{user_id}")
async def get_gender(user_id: int, gender_id: Gender | None = None):
    if gender_id:
        return {"user_id": user_id, "gender": gender_id.value}
    return {"user_id": user_id}


@app.post("/user/{user_id}")
async def add_gender(user_id: int, gender: Gender | None = None):
    return {"user_id": user_id, "new gender": gender.value}


class User(BaseModel):
    user_name: str
    user_age: int
    gender: Optional[Gender] = None
    email: str
    phone_number: str


@app.put("/user/{user_id}")
async def update_gender(user_id: int, user: User):
    return {"user_id": user_id, **user.model_dump()}
