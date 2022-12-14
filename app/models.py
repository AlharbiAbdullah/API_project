from sqlalchemy import (TIMESTAMP, Boolean, Column, ForeignKey,
                        Integer, String, text)
from .database import Base
from sqlalchemy.orm import relationship


# Posts model
class Post(Base):
    __tablename__ = 'posts' 

    id = Column(Integer , primary_key= True , nullable= False)
    title = Column(String , nullable = False)
    content = Column(String , nullable = False)
    published = Column(Boolean , server_default = 'True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False , 
                                    server_default=text('now()'))

    # Fkey
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    # creating a relationship 
    owner = relationship('User') 



# Users Models 

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key= True, nullable= False)
    email = Column(String, unique= True, nullable=False) 
    password= Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False , 
                                    server_default=text('now()'))


# Votes 
class Vote(Base):
    __tablename__= 'votes'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    