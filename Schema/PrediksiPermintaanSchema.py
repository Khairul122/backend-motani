from pydantic import BaseModel
from typing import Optional

class PrediksiPermintaanSchema(BaseModel):
    id_prediksi: int
    id_informasi: int
    wilayah: str
    periode: str
    deskripsi: Optional[str]

    model_config = {
        "from_attributes": True
    }

class PrediksiPermintaanCreateSchema(BaseModel):
    id_informasi: int
    wilayah: str
    periode: str
    deskripsi: Optional[str]
