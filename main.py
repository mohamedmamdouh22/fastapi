from fastapi import FastAPI, Query, Path
from enum import Enum
from typing import Annotated, Literal
from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/")
async def get():
    return {"message": "Hello World"}


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


@app.get("/user/{user_id}")
async def get_gender(
    user_id: Annotated[int, Path(..., ge=0)], gender_id: Annotated[Gender, Query(...)]
):
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
    user_dict = user.dict()
    if user_dict.get("gender") is not None:
        user_dict["gender"] = user_dict["gender"].value
    user_data = {"user_id": user_id, **user_dict}
    if limit:
        user_data.update({"limit": limit})
    return user_data


# create an end point to update the user data


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}
    start: int = Field(0, lt=100, ge=0)
    limit: int = Field(10, lt=100, ge=0)
    order_by: Literal["created_at", "updated_at"] = Field(
        default="created_at", title="Order by"
    )
    tags: list[str] = []


@app.put("/user/{user_id}")
async def update_user(
    *,
    user_id: Annotated[int, Path(..., gt=0, lt=100, title="User ID")],
    user: User,
    q: Annotated[FilterParams, Query(title="Query")],
):
    user_dict = user.dict()
    if q:
        user_dict.update(**q.dict())
    user_data = {"user_id": user_id, **user_dict}

    return user_data
