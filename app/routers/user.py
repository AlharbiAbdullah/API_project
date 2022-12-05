from .. import models, schemas, utils, oath2
from typing import List
from fastapi import ( FastAPI, status , 
                    HTTPException , Depends, APIRouter)
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix= '/users' , 
    tags= ['Users']
)

#get users 
@router.get('/' ,response_model= List[schemas.UserOut], 
                status_code= status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

#get users by id 
@router.get('/{id}', response_model= schemas.UserOut,
             status_code= status.HTTP_200_OK)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                detail=f'post with id: {id} was not found.')
    return user

#create user 
@router.post('/' , response_model= schemas.UserOut,
            status_code=status.HTTP_201_CREATED)
def create_user( user: schemas.UserCreate,
                 db: Session = Depends(get_db), 
                 current_user: int =  Depends(oath2.get_current_user)):
    # Hashing the password  - user.password 
    user.password = utils.hash(user.password)
    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Update a user 
@router.put('/{id}' , response_model=schemas.UserOut,
                     status_code= status.HTTP_202_ACCEPTED)
def update_user(id: int, user: schemas.UserCreate, 
                db: Session = Depends(get_db),
                current_user: int =  Depends(oath2.get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == id)
    if not db_user.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                detail=f'post with id: {id} was not found.')
    db_user.update(user.dict())
    db.commit()
    return db_user.first()

# Delete a user 
@router.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), 
                current_user: int =  Depends(oath2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                detail=f'post with id: {id} was not found.')
    db.delete(user.first())
    db.commit()
    return

