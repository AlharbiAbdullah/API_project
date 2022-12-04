from fastapi import (APIRouter, Depends, status, 
                        HTTPException, Response)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
from ..database import get_db 
from .. import schemas, models, utils, oath2

router = APIRouter(tags= ['Authentication'])

@router.post('/login')
def login(user_auth: OAuth2PasswordRequestForm = Depends(),
             db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_auth.username).first()
    #Verify email
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                            detail=f'Invalid Credentials')
    #verify password 
    if not utils.verify(user_auth.password , user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , 
                            detail=f'Invalid Credentials')
    
    # Return Token
    access_token = oath2.create_access_token(data = {
        'user_id': user.id
    })
    return {
        'Access Token: ': access_token , 
        'Token_type: ' : 'bearer'
    }

    