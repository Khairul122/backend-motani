# api/LoginController.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Model.LoginModel import LoginModel, User
from conn import get_db

router = APIRouter()

@router.post("/login/auth")
def auth(user: User, db: Session = Depends(get_db)):
    login_model = LoginModel(db)
    
    authenticated_user = login_model.authenticate_user(user)
    
    if authenticated_user:
        return {
            "message": "Login berhasil",
            "username": authenticated_user.username,
            "nama": authenticated_user.nama
        }
    else:
        raise HTTPException(status_code=400, detail="Username atau password salah")

@router.post("/logout")
def logout():
    return {"message": "Logout berhasil"}
