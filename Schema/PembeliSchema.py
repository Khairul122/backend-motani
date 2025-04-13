from pydantic import BaseModel
from typing import Optional

class PembeliSchema(BaseModel):
    id_pembeli: int
    id_users: int
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
    tgl_create: str

    class Config:
        orm_mode = True

# Schema khusus update (semua opsional)
class PembeliUpdateSchema(BaseModel):
    id_users: Optional[int] = None
    nama: Optional[str] = None
    no_telp: Optional[str] = None
    kecamatan: Optional[str] = None
    alamat: Optional[str] = None
    kodepos: Optional[str] = None
    tgl_lahir: Optional[str] = None
    jk: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    tgl_create: Optional[str] = None

    class Config:
        orm_mode = True
