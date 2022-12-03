from pydantic import BaseModel
from datetime import datetime

# pydantic model 
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

    class Config():
        orm_mode = True

# post response 
class PostResponse(PostBase):    
    created_at: datetime
    class Config():
        orm_mode = True

# get response 
class GetResponse(ResponseBase):
    # class Config():
    #     orm_mode = True
    pass