# api/LoginController.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Model.LoginModel import User, LoginModel
from conn import get_db

router = APIRouter()

@router.post("/login/auth")
def auth(user: User, db: Session = Depends(get_db)):
    login_model = LoginModel(db)
    
    # Memeriksa otentikasi pengguna
    authenticated_user = login_model.authenticate_user(user)
    
    if authenticated_user:
        # Kembalikan informasi otentikasi (bisa berupa token, atau sesi)
        return {
            "message": "Login berhasil",
            "username": authenticated_user.username,
            "nama": authenticated_user.nama,
            "level": authenticated_user.level,
            "status": authenticated_user.status
        }
    else:
        raise HTTPException(status_code=400, detail="Username atau password salah")

@router.post("/logout")
def logout():
    return {"message": "Logout berhasil"}
