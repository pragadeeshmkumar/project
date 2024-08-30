from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app import models, schemas, auth, database, middlewares

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.add_middleware(middlewares.LogMiddleware)

@app.post("/api/register", response_model=schemas.UserCreate)
def register(request: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = auth.pwd_context.hash(request.password_hash)
    db_user = models.User(username=request.username, email=request.email, password_hash=hashed_password, role=request.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/login")
def login(request: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not auth.pwd_context.verify(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token=auth.generate_token(data={'user_id':user.id})
    return {'access_token':access_token,'token_type':'bearer'}

@app.post("/api/posts")
def create_post(request: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if db_user.role not in [schemas.UserRole.admin, schemas.UserRole.author]:
        raise HTTPException(status_code=403)
    new_post = models.Post(title=request.title, content=request.content, author_id=current_user.id,created_at=datetime.now())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/api/posts")
def get_posts(author: Optional[str] = None, page: int = 1, db: Session = Depends(get_db)):
    query = db.query(models.Post)
    if author:
        query = query.join(models.User).filter(models.User.username == author)
    posts = query.offset((page-1)*2).limit(2).all()
    return posts

@app.post("/api/posts/{post_id}/comments")
def add_comment(post_id: int, comment: str, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404)
    new_comment = models.Comment(content=comment, post_id=post_id, user_id=current_user.id,created_at=datetime.now())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
