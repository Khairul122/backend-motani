from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conn import get_db
from Schema.LoginSchema import UserLogin
from Model.LoginModel import User
import globals

router = APIRouter()

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and user.password == password:
        return user
    return None

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_data = authenticate_user(db, user.username, user.password)
    if not user_data:
        raise HTTPException(status_code=401, detail="Username atau password salah")

    globals.current_user = user_data

    return {
        "message": "Login berhasil",
        "id_users": user_data.id_users,
        "name": user_data.name,
        "email": user_data.email,
        "username": user_data.username,
        "level": user_data.level
    }

@router.post("/logout")
def logout():
    globals.current_user = None
    return {"message": "Logout berhasil"}

@router.get("/me")
def get_current_user():
    if not globals.current_user:
        raise HTTPException(status_code=401, detail="Belum login")

    user = globals.current_user
    return {
        "id_users": user.id_users,
        "name": user.name,
        "email": user.email,
        "username": user.username,
        "level": user.level
    }
