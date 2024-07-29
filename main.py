from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy.orm import Session
from models import User
from fastapi import FastAPI, HTTPException, Depends
from schemas import UserBase

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.get('/users/{user_id}')
def get_user(user_id: int):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.close();
    return user

@app.post('/users/')
def create_user(user: UserBase):
    db_user = User(name=user.name, email=user.email, password=user.password)
    db: Session = SessionLocal()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user