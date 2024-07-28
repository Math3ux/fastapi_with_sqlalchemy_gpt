from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from fastapi import FastAPI, HTTPException;

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.get('/users/{user_id}')
def get_user(user_id: int):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.close();
    return user