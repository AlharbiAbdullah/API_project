from .. import models, schemas, oath2
from typing import List, Optional
from fastapi import ( FastAPI , status , 
                    HTTPException , Depends, APIRouter)
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix= '/posts', 
    tags= ['Posts']
) 

# GET posts 
#router.get('/', response_model= List[schemas.GetResponse],
@router.get('/',
         response_model= List[schemas.PostOut],
        status_code= status.HTTP_200_OK)
def get_posts(  db: Session = Depends(get_db),
                current_user: int =  Depends(oath2.get_current_user), 
                limit: int = 3, 
                skip: int = 0, 
                search: Optional[str] = ''):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes_count'))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search))\
        .limit(limit)\
        .offset(skip)\
        .all()
    return posts

# GET by ID 
@router.get('/{id}', response_model= schemas.PostOut,
            status_code = status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db),
            current_user: int =  Depends(oath2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes_count'))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                detail=f'post with id: {id} was not found.')
    return post

# Create 
@router.post('/' ,  response_model= schemas.PostResponse, 
            status_code=status.HTTP_201_CREATED)
def create_data(post: schemas.PostCreate, 
                db: Session = Depends(get_db),
                current_user: int =  Depends(oath2.get_current_user)):
    print(current_user.id)
    # To connect the user with data being posted, we get the ID from current_user
    # and append it to the dict
    new_post = models.Post(owner_id= current_user.id , **post.dict())
    db.add(new_post)
    db.commit()

    # to retrive the data and return it to the user we need to refresh 
    db.refresh(new_post)
    return new_post

# Delete 
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int =  Depends(oath2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                detail=f'post with id: {id} was not found.')
    # check if the user own the post 
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= 'not authorized to preforme requested action')
    db.delete(post)
    db.commit()
    return 

# Update
@router.put('/{id}', status_code= status.HTTP_202_ACCEPTED)
def update_post(id: int, post: schemas.PostCreate, 
                db: Session = Depends(get_db) , 
                current_user: int =  Depends(oath2.get_current_user)):

    query = db.query(models.Post).filter(models.Post.id == id)
    record = query.first()

    if not record:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                                detail=f'post with id: {id} was not found.')
    # If user not authorized to make chenges 
    if record.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= 'not authorized to preforme requested action')
    query.update(post.dict(), synchronize_session= False)
    db.commit()
    return query.first()
