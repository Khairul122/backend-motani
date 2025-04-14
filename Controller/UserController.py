from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from conn import SessionLocal
from typing import List

from Model.LoginModel import User                         
from Schema.UserSchema import UserSchema            

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users/", response_model=List[UserSchema])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/users/{id_users}", response_model=UserSchema)
def get_user_by_id(id_users: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id_users == id_users).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{id_users}")
def delete_user(id_users: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id_users == id_users).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"detail": f"User dengan ID {id_users} berhasil dihapus"}