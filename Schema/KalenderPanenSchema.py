from pydantic import BaseModel
from datetime import date
from typing import Optional

class KalenderPanenSchema(BaseModel):
    id_kalender: int
    id_informasi: int
    wilayah: str
    awal_panen: date
    akhir_panen: date
    catatan: Optional[str]

    model_config = {
        "from_attributes": True
    }

class KalenderPanenCreateSchema(BaseModel):
    id_informasi: int
    wilayah: str
    awal_panen: date
    akhir_panen: date
    catatan: Optional[str]
