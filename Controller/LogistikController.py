from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from conn import SessionLocal
from Model.LogistikModel import Logistik
from Model.LoginModel import User
from Schema.LogistikSchema import LogistikSchema, LogistikCreateSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/logistik/", response_model=List[LogistikSchema])
def get_all_logistik(db: Session = Depends(get_db)):
    return db.query(Logistik).all()

@router.get("/logistik/{id}", response_model=LogistikSchema)
def get_logistik_by_id(id: int, db: Session = Depends(get_db)):
    logistik = db.query(Logistik).filter(Logistik.id == id).first()
    if not logistik:
        raise HTTPException(status_code=404, detail="Logistik not found")
    return logistik

@router.put("/logistik/{id}", response_model=LogistikSchema)
def update_logistik(id: int, data: LogistikCreateSchema, db: Session = Depends(get_db)):
    logistik = db.query(Logistik).filter(Logistik.id == id).first()
    if not logistik:
        raise HTTPException(status_code=404, detail="Logistik not found")

    for key, value in data.dict().items():
        setattr(logistik, key, value)

    db.commit()
    db.refresh(logistik)
    return logistik

@router.delete("/logistik/{id}")
def delete_logistik(id: int, db: Session = Depends(get_db)):
    logistik = db.query(Logistik).filter(Logistik.id == id).first()
    if not logistik:
        raise HTTPException(status_code=404, detail="Logistik not found")

    user = db.query(User).filter(User.id_users == logistik.id_users).first()

    db.delete(logistik)

    if user:
        db.delete(user)

    db.commit()
    return {"detail": f"Logistik dan User terkait dengan ID {id} berhasil dihapus"}