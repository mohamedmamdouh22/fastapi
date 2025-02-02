from fastapi import FastAPI, Query, Path, Body
from enum import Enum
from typing import Annotated, Literal
from pydantic import BaseModel, Field, HttpUrl

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


class Photo(BaseModel):
    url: HttpUrl
    name: str


class User(BaseModel):
    user_name: str
    user_age: int
    gender: Gender | None = None
    email: str
    phone_number: str
    photos: list[Photo]


class Class(BaseModel):
    class_name: str | None = Field(default="Python", title="Class Name")
    class_location: str | None = Field(default="Online", title="Class Location")


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
    user: Annotated[User, Body(..., title="User")],
    class_body: Annotated[Class | None, Body(title="Class")] = None,
    q: Annotated[FilterParams, Query(title="Query")],
    importance: Annotated[int, Body(title="Importance")],
):
    user_dict = user.model_dump()
    if q:
        user_dict.update(**q.model_dump())
    user_data = {"user_id": user_id, **user_dict}
    if class_body:
        user_data.update(**class_body.model_dump())
    return user_data
