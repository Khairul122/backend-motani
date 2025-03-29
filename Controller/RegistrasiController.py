from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conn import get_db
from Schema.RegistrasiSchema import RegistrasiAdmin, RegistrasiPembeli, RegistrasiLogistik
from Model.RegistrasiModel import (
    RegistrasiAdministrator as SimpanAdmin,
    RegistrasiPembeli as SimpanPembeli,
    RegistrasiLogistik as SimpanLogistik
)
from Model.LoginModel import User

router = APIRouter()

@router.post("/register/admin")
def RegistrasiAdministrator(data: RegistrasiAdmin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username atau email sudah terdaftar")

    new_admin = SimpanAdmin(db, data)

    return {
        "message": "Registrasi administrator berhasil",
        "data": {
            "id_users": new_admin.id_users,
            "name": new_admin.name,
            "email": new_admin.email,
            "username": new_admin.username,
            "level": new_admin.level
        }
    }

@router.post("/register/pembeli")
def RegistrasiPembeli(data: RegistrasiPembeli, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username atau email sudah terdaftar")

    pembeli = SimpanPembeli(db, data)

    return {
        "message": "Registrasi pembeli berhasil",
        "data": {
            "id_pembeli": pembeli.id_pembeli,
            "nama": pembeli.nama,
            "email": pembeli.email,
            "username": pembeli.username
        }
    }

@router.post("/register/logistik")
def RegistrasiLogistik(data: RegistrasiLogistik, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username atau email sudah terdaftar")

    logistik = SimpanLogistik(db, data)

    return {
        "message": "Registrasi logistik berhasil",
        "data": {
            "id_logistik": logistik.id,
            "nama": logistik.nama,
            "nama_toko": logistik.nama_toko,
            "email": data.email,
            "username": data.username,
            "status": logistik.status
        }
    }