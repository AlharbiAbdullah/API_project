from passlib.context import CryptContext


# Setting up the hashing alogrithims 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated= 'auto')

def hash(password: str):
    return pwd_context.hash(password)


# Verfiy the user hashed password when login 

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    