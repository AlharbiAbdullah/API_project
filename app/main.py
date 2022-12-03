from typing import List
from fastapi import (FastAPI , Response ,
                     status , HTTPException , Depends )
# Using pydantic to create schema and for validations 
from fastapi import Body 
import psycopg2
# to include the column name we need to use RealDictCursor
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine , get_db

## Creating SQLAlchemy enging 
models.Base.metadata.create_all(bind=engine)

app = FastAPI() 



# GET 
@app.get('/')
def root():
    return {"API" : "root"}


# GET posts 
@app.get('/posts', response_model= List[schemas.GetResponse],
        status_code= status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all() 
    return posts

# GET by ID 
@app.get('/posts/{id}', response_model= schemas.GetResponse,
            status_code = status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                detail=f'post with id: {id} was not found.')
    return post


# Create 
@app.post('/posts' ,  response_model= schemas.PostResponse, 
            status_code=status.HTTP_201_CREATED)
def create_data(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()

    # to retrive the data and return it to the user we need to refresh 
    db.refresh(new_post)
    return new_post

# Delete 
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                detail=f'post with id: {id} was not found.')
    db.delete(post.first())
    db.commit()
    return 

# Update
@app.put('/posts/{id}', status_code= status.HTTP_202_ACCEPTED)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    query = db.query(models.Post).filter(models.Post.id == id)

    if not query.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                detail=f'post with id: {id} was not found.')

    query.update(post.dict(), synchronize_session= False)
    db.commit()
    return query.first()

"""
Starting webserver with uvicorn 

 terminal: uvicorn main:app 
""" 



