from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from conn import Base

class PrediksiPermintaan(Base):
    __tablename__ = "prediksi_permintaan"
    __table_args__ = {'extend_existing': True}

    id_prediksi = Column(Integer, primary_key=True, autoincrement=True)
    id_informasi = Column(Integer, ForeignKey("informasi.id_informasi"))
    wilayah = Column(String(100))
    periode = Column(String(50))
    deskripsi = Column(Text)

    informasi = relationship("Informasi", backref="prediksi_permintaan")
