from fastapi import FastAPI,HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt,JWTError
from . import models, schemas, database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY='32db92a32a3f14df9e89e0bef46ed21fa6a9a8c678a3d8b178693b1c1f2506ae'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=20
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='api/login')

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_token(data:dict):
    to_encode=data.copy()
    expire = datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
        user = db.query(models.User).filter(models.User.id == token_data.id).first()
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user
