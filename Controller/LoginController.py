# Controller/LoginController.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Model.LoginModel import User, LoginModel, RegistrasiKonsumen, RegistrasiLogistik
from conn import get_db
from datetime import datetime

router = APIRouter()

@router.post("/login/konsumen")
def login_konsumen(user: User, db: Session = Depends(get_db)):
    login_model = LoginModel(db)
    authenticated_user = login_model.authenticate_konsumen(user)
    if authenticated_user:
        return {
            "status": True,
            "message": "Login berhasil",
            "payload": authenticated_user
        }
    else:
        raise HTTPException(status_code=404, detail="Username atau password salah")

@router.post("/login/logistik")
def login_logistik(user: User, db: Session = Depends(get_db)):
    login_model = LoginModel(db)
    authenticated_user = login_model.authenticate_logistik(user)
    if authenticated_user:
        return {
            "status": True,
            "message": "Login berhasil",
            "payload": authenticated_user
        }
    else:
        raise HTTPException(status_code=404, detail="Username atau password salah")

@router.post("/registrasi/konsumen")
def registrasi_konsumen(data: RegistrasiKonsumen, db: Session = Depends(get_db)):
    login_model = LoginModel(db)
    if db.query(KonsumenInDB).filter(KonsumenInDB.no_telp == data.no_telp).first():
        raise HTTPException(status_code=400, detail="Nomor telepon sudah terdaftar")
    params = {
        'no_telp': data.no_telp,
        'password': data.no_telp,  # Asumsikan password sama dengan nomor telepon untuk demo
        'nama': data.nama,
        'tgl_create': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'alamat': data.alamat,
        'tgl_lahir': data.tgl_lahir,
        'jk': data.jk,
        'email': data.email
    }
    new_konsumen = login_model.registrasi_konsumen(params)
    return {
        "status": True,
        "message": "Registrasi berhasil",
        "payload": new_konsumen
    }

@router.post("/registrasi/logistik")
def registrasi_logistik(data: RegistrasiLogistik, db: Session = Depends(get_db)):
    login_model = LoginModel(db)
    if db.query(LogistikInDB).filter(LogistikInDB.no_hp == data.no_hp).first():
        raise HTTPException(status_code=400, detail="Nomor HP sudah terdaftar")
    params = {
        'no_hp': data.no_hp,
        'password': data.password,
        'nama_toko': data.nama_toko,
        'alamat': data.alamat,
        'lat': data.lat,
        'lng': data.lng,
        'status': data.status
    }
    new_logistik = login_model.registrasi_logistik(params)
    return {
        "status": True,
        "message": "Registrasi logistik berhasil",
        "payload": new_logistik
    }

@router.post("/ubahpassword/konsumen")
def ubah_password_konsumen(user: User, db: Session = Depends(get_db)):
    login_model = LoginModel(db)
    konsumen = db.query(KonsumenInDB).filter(KonsumenInDB.no_telp == user.username).first()
    if konsumen:
        konsumen.password = user.password
        db.commit()
        return {
            "status": True,
            "message": "Password berhasil diubah"
        }
    else:
        raise HTTPException(status_code=404, detail="Konsumen tidak ditemukan")

@router.post("/ubahpassword/logistik")
def ubah_password_logistik(user: User, db: Session = Depends(get_db)):
    login_model = LoginModel(db)
    logistik = db.query(LogistikInDB).filter(LogistikInDB.no_hp == user.username).first()
    if logistik:
        logistik.password = user.password
        db.commit()
        return {
            "status": True,
            "message": "Password logistik berhasil diubah"
        }
    else:
        raise HTTPException(status_code=404, detail="Logistik tidak ditemukan")
