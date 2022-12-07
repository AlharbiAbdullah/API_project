from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
# Using pydantic to create schema and for validations 

# pydantic model 



#returning users 
# user out has to be above posts becuase we want to retrive users within posts 
class UserOut(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

    class Config():
        orm_mode = True

# User model 
class UserCreate(BaseModel):
    email: EmailStr
    password: str 


# posts 
class PostBase(BaseModel):
    title: str 
    content: str 
    published: bool = True

#create or update 
class PostCreate(PostBase):
    pass


# Response model
class ResponseBase(BaseModel):
    title: str 
    content: str
    owner_id: str
    owner: UserOut 

    class Config():
        orm_mode = True

# post response 
class PostResponse(PostBase):    
    created_at: datetime
    class Config():
        orm_mode = True

# get response 
class GetResponse(ResponseBase):
    pass

# Posts with votes 
class PostOut(BaseModel):
    Post: ResponseBase
    votes_count: int

    class Config():
        orm_mode = True

# Login class 

class Login(BaseModel):
    email: EmailStr 
    password: str


# Access token schema 

class Token(BaseModel): 
    access_token: str 
    token_type: str 

class TokenData(BaseModel):
    id: Optional[str] = None

# Voting schema 

class Vote(BaseModel):
    post_id: int 
    # conint -> to inforce the dir to be 0 or 1
    dir: conint(ge=0, le=1) 

     

