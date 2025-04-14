from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal

class ProdukFotoSchema(BaseModel):
    id_foto: int
    id_produk: int
    url_foto: str

    model_config = {
        "from_attributes": True
    }

class ProdukSchema(BaseModel):
    id_produk: int
    nama_produk: str
    keterangan: Optional[str]
    stok: int
    deskripsi: Optional[str]
    status_produk: Optional[str]
    id_logistik: int
    harga: Decimal
    diskon: Decimal
    produk_foto: List[ProdukFotoSchema] = []

    model_config = {
        "from_attributes": True
    }

class ProdukCreateSchema(BaseModel):
    nama_produk: str
    keterangan: Optional[str]
    stok: Optional[int] = 0
    deskripsi: Optional[str]
    status_produk: Optional[str] = "aktif"
    id_logistik: int
    harga: Decimal
    diskon: Optional[Decimal] = 0.00

    model_config = {
        "from_attributes": True
    }
