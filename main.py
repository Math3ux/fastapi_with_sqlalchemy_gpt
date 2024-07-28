from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from fastapi import FastAPI;

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.get('/users/{user_id}')
def get_user(user_id: int):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user == None:
        return {'message': 'User not found'}
    db.close();
    return user