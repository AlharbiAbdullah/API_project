from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

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

     

