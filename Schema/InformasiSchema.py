from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from Schema.KalenderPanenSchema import KalenderPanenSchema
from Schema.PrediksiPermintaanSchema import PrediksiPermintaanSchema

class InformasiSchema(BaseModel):
    id_informasi: int
    judul: str
    ket: Optional[str] = None
    tgl_post: date
    foto: Optional[str] = None
    kalender_panen: List[KalenderPanenSchema] = []
    prediksi_permintaan: List[PrediksiPermintaanSchema] = []

    model_config = {
        "from_attributes": True
    }

class InformasiCreateSchema(BaseModel):
    judul: str
    ket: Optional[str] = None
    tgl_post: date
    foto: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class InformasiUpdateSchema(BaseModel):
    judul: Optional[str] = None
    ket: Optional[str] = None
    tgl_post: Optional[date] = None
    foto: Optional[str] = None

    model_config = {
        "from_attributes": True
    }