from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#uvicorn main:app --reload


app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    email: str
    
users = [
    User(id=1, username="Danil", email="user1@gmail.com"),
    User(id=2, username="Rayan", email="user2@gmail.com")
]

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/users", response_model=list[User])
def get_users():
    return users

@app.post("/create_user", response_model=User)
def create_user(user: User):
    users.append(user)
    return user