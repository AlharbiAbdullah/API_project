from fastapi import FastAPI 
from . import models
from .database import engine 
from .routers import post , user, auth, vote


## Creating SQLAlchemy enging 
models.Base.metadata.create_all(bind=engine)

app = FastAPI() 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# GET 
@app.get('/')
def root():
    return {"API" : "root"}


"""
Starting webserver with uvicorn 

 terminal: uvicorn main:app 
""" 



