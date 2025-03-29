from pydantic import BaseModel
from typing import Literal

class RegistrasiAdmin(BaseModel):
    name: str
    email: str
    username: str
    password: str
    level: str

class RegistrasiPembeli(BaseModel):
    nama: str
    no_telp: str
    kecamatan: str
    alamat: str
    kodepos: str
    tgl_lahir: str
    jk: str
    email: str
    username: str
    password: str

class RegistrasiLogistik(BaseModel):
    nama: str
    no_hp: str
    alamat: str
    nama_toko: str | None = None
    lat: float
    lng: float
    email: str
    username: str
    password: str
    status: Literal["penjual", "roasting", "pengepul"]