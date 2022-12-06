from fastapi import FastAPI 
from . import models
from .database import engine 
from .routers import post , user, auth

## Creating SQLAlchemy enging 
models.Base.metadata.create_all(bind=engine)

app = FastAPI() 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# GET 
@app.get('/')
def root():
    return {"API" : "root"}


"""
Starting webserver with uvicorn 

 terminal: uvicorn main:app 
""" 



