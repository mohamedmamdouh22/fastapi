from fastapi import FastAPI, Query
from enum import Enum
from typing import Annotated
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


class User(BaseModel):
    user_name: str
    user_age: int
    gender: Gender | None = None
    email: str
    phone_number: str


@app.post("/user/{user_id}")
async def update_gender(user_id: int, user: User, limit: int | None = None):
    user_dict = user.model_dump()
    if user_dict.get("gender") is not None:
        user_dict["gender"] = user_dict["gender"].value
    user_data = {"user_id": user_id, **user_dict}
    if limit:
        user_data.update({"limit": limit})
    return user_data


# create an end point to update the user data


@app.put("/user/{user_id}")
async def update_user(
    user_id: int,
    user: User,
    q: Annotated[str, Query(max_length=10, alias="query")] = ...,
):
    user_dict = user.model_dump()
    if q:
        user_dict.update({"q": q})
    user_data = {"user_id": user_id, **user_dict}
    return user_data
