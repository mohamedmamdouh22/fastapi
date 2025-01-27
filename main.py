from fastapi import FastAPI
from enum import Enum

app = FastAPI()


@app.get("/")
async def get():
    return {"message": "Fuck Fe Fe"}



@app.post("/user/{user_id}")
async def update_user(user_id: int, user_data: dict):
    user_data["user_id"] = user_id
    return {"user_id": user_id, "user_data": user_data}


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


@app.get("/user/{user_id}")
async def get_gender(user_id: int, gender_id: Gender | None = None):
    if gender_id:
        return {"user_id": user_id, "gender": gender_id.value}
    return {'user_id':user_id}

@app.post("/user/{user_id}/{gender}")
async def update_gender(user_id: int, gender: Gender):
    return {"user_id": user_id, "new gender": gender.value}
