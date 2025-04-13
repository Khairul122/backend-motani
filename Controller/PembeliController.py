from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from conn import SessionLocal
from Model.PembeliModel import Pembeli
from Model.LoginModel import User
from Schema.UserSchema import UserSchema, UserCreateSchema, UserUpdateSchema
from typing import List
from Schema.PembeliSchema import PembeliSchema, PembeliUpdateSchema
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/pembeli/", response_model=List[PembeliSchema])
def get_all_pembeli(db: Session = Depends(get_db)):
    return db.query(Pembeli).all()

@router.get("/pembeli/{id_pembeli}", response_model=PembeliSchema)
def get_pembeli_by_id(id_pembeli: int, db: Session = Depends(get_db)):
    pembeli = db.query(Pembeli).filter(Pembeli.id_pembeli == id_pembeli).first()
    if pembeli is None:
        raise HTTPException(status_code=404, detail="Pembeli not found")
    return pembeli

@router.post("/pembeli/", response_model=PembeliSchema)
def create_pembeli(pembeli_data: PembeliSchema, db: Session = Depends(get_db)):
    pembeli = Pembeli(**pembeli_data.dict())
    db.add(pembeli)
    db.commit()
    db.refresh(pembeli)
    return pembeli

@router.put("/pembeli/{id_pembeli}", response_model=PembeliSchema)
def update_pembeli(id_pembeli: int, pembeli_data: PembeliUpdateSchema, db: Session = Depends(get_db)):
    pembeli = db.query(Pembeli).filter(Pembeli.id_pembeli == id_pembeli).first()
    if pembeli is None:
        raise HTTPException(status_code=404, detail="Pembeli not found")

    pembeli_data_dict = pembeli_data.dict(exclude_unset=True)
    for key, value in pembeli_data_dict.items():
        setattr(pembeli, key, value)

    db.commit()
    db.refresh(pembeli)
    return pembeli
@router.delete("/pembeli/{id_pembeli}")
def delete_pembeli(id_pembeli: int, db: Session = Depends(get_db)):
    pembeli = db.query(Pembeli).filter(Pembeli.id_pembeli == id_pembeli).first()

    if pembeli is None:
        raise HTTPException(status_code=404, detail="Pembeli not found")

    user = db.query(User).filter(User.id_users == pembeli.id_users).first()

    db.delete(pembeli)

    if user:
        db.delete(user)

    db.commit()

    return {"detail": "Pembeli dan User terkait berhasil dihapus"}
