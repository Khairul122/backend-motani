from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProduksiSchema(BaseModel):
    id_produksi: int
    id_produk: int
    tanggal_panen: Optional[date]
    tanggal_roasting: Optional[date]
    jumlah: int
    jenis_varietas: Optional[str]
    nama_pemasok: Optional[str]
    catatan: Optional[str]
    status_produksi: Optional[str]

    model_config = {
        "from_attributes": True
    }

class ProduksiCreateSchema(BaseModel):
    id_produk: int
    tanggal_panen: Optional[date]
    tanggal_roasting: Optional[date]
    jumlah: int
    jenis_varietas: Optional[str]
    nama_pemasok: Optional[str]
    catatan: Optional[str]
    status_produksi: Optional[str]

    model_config = {
        "from_attributes": True
    }
