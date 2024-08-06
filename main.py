from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy.orm import Session
from models import User
from fastapi import FastAPI, HTTPException, Depends
from schemas import UserBase, UserUpdate

app = FastAPI()

user_exception_message = "User not found"


@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.get('/users/')
def get_all_users():
    db: Session = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

@app.get('/users/{user_id}')
def get_user(user_id: int):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=user_exception_message)
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

@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=user_exception_message)
    db.delete(user)
    db.commit()
    db.close()
    return user

@app.patch('/users/{user_id}')
def update_user(user_id: int, user_query: UserUpdate):
    db: Session = SessionLocal()
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail=user_exception_message)

    for key, value in user_query.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user
