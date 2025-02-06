from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from enum import Enum
from uuid import UUID
from datetime import datetime, timedelta, time
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


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Photo]):
    return images


# declare request example data
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(..., gt=0, title="Item ID")],
    item: Annotated[
        Item,
        Body(
            ...,
            title="Item",
            openapi_examples={
                "normal item": {
                    "summary": "An example of a normal item",
                    "description": "This is an example of a normal item that should be returned",
                    "value": {
                        "name": "Item 1",
                        "description": "Item 1 description",
                        "price": 100.0,
                        "tax": 10.0,
                    },
                },
                "converted item": {
                    "summary": "An example of a converted item",
                    "description": "This is an example of a converted item that FastApi will convert the price from string to number",
                    "value": {
                        "name": "Item 2",
                        "description": "Item 2 description",
                        "price": "200",
                    },
                },
                "invalid item": {
                    "summary": "An example of an invalid item",
                    "description": "This is an example of an invalid item that FastApi will raise an error",
                    "value": {
                        "name": "Item 3",
                        "description": "Item 3 description",
                        "price": "fifteen dollars",
                        "tax": "ten dollars",
                    },
                },
            },
        ),
    ],
):
    return {"item_id": item_id, **item.model_dump()}


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }


class Cookies(BaseModel):
    Aws_token: Annotated[str | None, Cookie()] = None
    session_id: Annotated[str | None, Cookie()] = None


@app.get("/items/")
async def return_items(
    *,
    cookies: Annotated[Cookies, Cookie()],
    accept_encoding: str | None = Header(None, title="Accept Encoding"),
    accept_language: str | None = Header(None, title="Accept Language"),
    sec_ch_ua: str | None = Header(None, title="Sec Ch Ua"),
    user_agent: str | None = Header(None, title="User Agent"),
):
    if cookies:
        return {
            "Aws_token": cookies.Aws_token,
            "session_id": cookies.session_id,
            "accept_encoding": accept_encoding,
            "accept_language": accept_language,
            "sec_ch_ua": sec_ch_ua,
        }
    return {
        "accept_encoding": accept_encoding,
        "accept_language": accept_language,
        "sec_ch_ua": sec_ch_ua,
        "user_agent": user_agent,
    }


class Headers(BaseModel):
    accept_encoding: Annotated[str | None, Header()] = None
    accept_language: Annotated[str | None, Header()] = None
    sec_ch_ua: Annotated[str | None, Header()] = None
    user_agent: Annotated[str | None, Header()] = None


@app.get("/items/with-headers")
async def return_items_with_headers(headers: Annotated[Headers, Header()]):
    return {
        "accept_encoding": headers.accept_encoding,
        "accept_language": headers.accept_language,
        "sec_ch_ua": headers.sec_ch_ua,
        "user_agent": headers.user_agent,
    }
