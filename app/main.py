from pyexpat import model
from typing import Optional
from fastapi import (FastAPI , Response ,
                     status , HTTPException , Depends )
# Using pydantic to create schema and for validations 
from pydantic import BaseModel
import psycopg2
# to include the column name we need to use RealDictCursor
from psycopg2.extras import RealDictCursor
import time 
from . import models
from .database import SessionLocal, enging
from sqlalchemy.orm import Session

app = FastAPI() 

## Creating SQLAlchemy enging 
model.Base.metadata.create_all(bind=enging)

# Dependinses 
def get_db():
    db =  SessionLocal() 
    try:
        yield db 
    finally:
        db.close()

# Setting up DB connection 

# While loop to loop until the connection is succesfull
# Because we dont want to let api work untill we connect to the DB
while True:

    try:
        conn = psycopg2.connect(
            host='localhost' , 
            database= 'fastAPI' , 
            user='postgres' , 
            password='@!Alaa2233' , 
            cursor_factory= RealDictCursor
        )
        cursor = conn.cursor()
        print('Database connection was succesfull')
        break

    except Exception as error:
        print('connection to the Database failed')
        print('Error: ' , error)
        time.sleep(5)

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

# to be removed: getting the id for /posts/id 

def find_id(id):
    for p in my_posts:
        if p['id'] == id:
            return p 
        

# GET 
@app.get('/')
def root():
    return {"data" : "new_post"}


# GET posts 
@app.get('/posts')
def get_posts():
    cursor.execute("""
            SELECT *
            FROM public.POSTS
            """)
    posts = cursor.fetchall()
    return {
        'data' : posts 
    }



# GET by ID 
@app.get('/posts/{id}')
def get_post(id: int , response: Response):
    cursor.execute(f""" 
                        SELECT 
                            *
                        FROM 
                            POSTS 
                        WHERE 
                            Id = {id}""")
    post = cursor.fetchall()

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


# For testing sqlalchemy 

app.get('/sal')
def test_post(db: Session = Depends(get_db)):
    return {'status' : 'Good'}


# Starting webserver with uvicorn 

# bash: uvicorn main:app 



