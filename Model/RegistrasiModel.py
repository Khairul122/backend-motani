from sqlalchemy.orm import Session
from Model.LoginModel import User
from Schema.RegistrasiSchema import RegistrasiAdmin, RegistrasiPembeli, RegistrasiLogistik
from Model.PembeliModel import Pembeli
from Model.LogistikModel import Logistik
from datetime import datetime

def RegistrasiAdministrator(db: Session, data: RegistrasiAdmin):
    admin = User(
        name=data.name,
        email=data.email,
        username=data.username,
        password=data.password,
        level=data.level
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

def RegistrasiPembeli(db: Session, data: RegistrasiPembeli):
    user = User(
        name=data.nama,
        email=data.email,
        username=data.username,
        password=data.password,
        level='Pembeli'
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    tgl_create = datetime.now().strftime("%d-%m-%Y")

    pembeli = Pembeli(
        id_pembeli=user.id_users,
        id_users=user.id_users,
        nama=data.nama,
        no_telp=data.no_telp,
        kecamatan=data.kecamatan,
        alamat=data.alamat,
        kodepos=data.kodepos,
        tgl_lahir=data.tgl_lahir,
        jk=data.jk,
        email=data.email,
        username=data.username,
        password=data.password,
        tgl_create=tgl_create
    )
    db.add(pembeli)
    db.commit()
    db.refresh(pembeli)

    return pembeli

def RegistrasiLogistik(db: Session, data: RegistrasiLogistik):
    user = User(
        name=data.nama,
        email=data.email,
        username=data.username,
        password=data.password,
        level="Logistik"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logistik = Logistik(
        id_users=user.id_users,
        nama=data.nama,
        no_hp=data.no_hp,
        alamat=data.alamat,
        nama_toko=data.nama_toko,
        lat=data.lat,
        lng=data.lng,
        status=data.status
    )
    db.add(logistik)
    db.commit()
    db.refresh(logistik)

    return logistik