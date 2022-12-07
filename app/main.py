from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine 
from .routers import post , user, auth, vote


# Since we use Alembic for DDL, we don't need this line
## Creating SQLAlchemy enging 
#models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

# CORS 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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



