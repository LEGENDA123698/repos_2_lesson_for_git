from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
#uvicorn main:app --reload


app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    email: str
    
# users = [
#     User(id=1, username="Danil", email="user1@gmail.com"),
#     User(id=2, username="Rayan", email="user2@gmail.com")
# ]

# @app.get("/users/{user_id}", response_model=User)
# def get_user(user_id: int):
#     for user in users:
#         if user.id == user_id:
#             return user
#     raise HTTPException(status_code=404, detail="User not found")

# @app.get("/users", response_model=list[User])
# def get_users():
#     return users

# @app.post("/create_user", response_model=User)
# def create_user(user: User):
#     users.append(user)
#     return user


conn = sqlite3.connect('users.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT,
                   email TEXT
                )''')
conn.commit()


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    if user:
        return {"id": user[0], "username": user[1], "email": user[2]}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/users")
async def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return users   

@app.post("/create_user")
async def create_user(user: User):
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (user.username, user.email))
    conn.commit()
    return user