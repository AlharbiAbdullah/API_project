from typing import Optional
from fastapi import (FastAPI , Response ,
                     status , HTTPException , Depends )
# Using pydantic to create schema and for validations 
from fastapi import Body 
from pydantic import BaseModel
import psycopg2
# to include the column name we need to use RealDictCursor
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models 
from .database import engine , get_db

## Creating SQLAlchemy enging 
models.Base.metadata.create_all(bind=engine)

app = FastAPI() 


# Schema definition  
class Post(BaseModel):
    title: str 
    content: str 
    # Published -> it's an optional for the user to fill, 
    # We default the value as True 
    published: bool = True
    # If we want the default value is None so we dont store any values
        # if the user didn't provide it. 
    rating: Optional[int] = None 

# Save data locally at the moment; then Ideally I would save at a DB
my_posts = [
    {
        "title" : "title of post 1" , 
        "content" : "content of post 1" ,
        "id" : 1
    } ,
    {
        "title" : "title of post 2" , 
        "content" : "content of post 2" , 
        "id" : 2 
    }
] 



# GET 
@app.get('/')
def root():
    return {"data" : "new_post"}


# GET posts 
@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all() 
    return{
        'data' : posts
    }


# GET by ID 
@app.get('/posts/{id}')
def get_post(id: int , status_code = status.HTTP_200_OK,
            db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                detail=f'post with id: {id} was not found.')
    return {
        'post_details' : post 
    }


# POST
@app.post('/posts' , status_code=status.HTTP_201_CREATED)
def create_data(post: Post):
    cursor.execute(""" INSERT INTO 
                            POSTS 
                                (title , content , published) 
                            VALUES 
                                (%s , %s , %s) RETURNING * """ , 
                                (post.title , post.content , post.published))
    new_post = cursor.fetchone()

    # To commit the insert 
    conn.commit() 
    return {
        "new_data" : new_post
    }

"""
Starting webserver with uvicorn 

 terminal: uvicorn main:app 
"""

