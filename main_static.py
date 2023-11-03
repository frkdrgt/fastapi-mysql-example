##pip install sqlalchemy pymysql fastapi uvicorn[standard]
##pip install "python-jose[cryptography]"
##pip install "passlib[bcrypt]"
#pip install python-multipart 
#python -m uvicorn main:app --reload
from fastapi import FastAPI, HTTPException
from typing import List
from models import Gender, User, UserUpdateRequest
from uuid  import UUID, uuid4

app = FastAPI()

db:List[User] = [
    User(id=uuid4(),first_name="Faruk",last_name="Durgut",gender=Gender.male),
    User(id=uuid4(),first_name="Ömer",last_name="Durgut",gender=Gender.male)
]

@app.get("/")
async def root():
    return {"Hello":"Mundo"}


@app.get("/api/v1/users")
async def fetch_users():
    return db;


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id:UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    
    raise HTTPException(
        status_code= 404,
        detail=f"user with id:{user_id} does not exists"
    )
    
@app.put("/api/v1/users/{user_id}")
async def update_user(request: UserUpdateRequest, user_id : UUID):
    for user in db:
        if user.id == user_id:
            if request.first_name is not None:
                user.first_name = request.first_name
                
    raise HTTPException(
        status_code=404,
        detail="user does not exist"
    )