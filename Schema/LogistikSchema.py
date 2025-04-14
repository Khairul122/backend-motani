from pydantic import BaseModel
from typing import Optional, Literal

class LogistikSchema(BaseModel):
    id: int
    nama: str
    no_hp: str
    alamat: str
    nama_toko: Optional[str]
    lat: float
    lng: float
    id_users: int
    status: Literal['penjual', 'roasting', 'pengepul']

    model_config = {
        "from_attributes": True
    }

class LogistikCreateSchema(BaseModel):
    nama: str
    no_hp: str
    alamat: str
    nama_toko: Optional[str]
    lat: float
    lng: float
    id_users: int
    status: Literal['penjual', 'roasting', 'pengepul']

    model_config = {
        "from_attributes": True
    }
