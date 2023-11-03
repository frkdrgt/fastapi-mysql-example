from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import entities
from database import engine,SessionLocal
from sqlalchemy.orm import Session
import auth 

app = FastAPI()
app.include_router(auth.router)

entities.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title:str
    content:str
    user_id:int
    
class UserBase(BaseModel):
    username:str
    password:str
    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(auth.get_current_user)]

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db:db_dependency):
    #db_user = entities.User(**user.model_dump())
    db_user = entities.User(
        username= user.username,
        password= auth.bcrypt_context.hash(user.password)
    )
    db.add(db_user)
    db.commit()
    
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id:int, db:db_dependency, current_user:user_dependency):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="No auth")
    user = db.query(entities.User).filter(entities.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post(post:PostBase, db:db_dependency):
    db_post = entities.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    
@app.get("/posts/{post_id}",status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    post = db.query(entities.Post).filter(entities.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404,detail="post not found")
    return post

@app.delete("/posts/{post_id}",status_code=status.HTTP_200_OK)
async def delete_post(post_id:int, db: db_dependency):
    db_post =  db.query(entities.Post).filter(entities.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404,detail="post not found")
    db.delete(db_post)
    db.commit()
