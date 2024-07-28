from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from fastapi import FastAPI;

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Hello World'}
