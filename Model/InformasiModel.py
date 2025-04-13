from sqlalchemy import Column, Integer, String, Text, Date
from conn import Base

class Informasi(Base):
    __tablename__ = "informasi"
    __table_args__ = {'extend_existing': True}

    id_informasi = Column(Integer, primary_key=True, autoincrement=True)
    judul = Column(String(255), nullable=False)
    ket = Column(Text)
    tgl_post = Column(Date, nullable=False)
    foto = Column(String(500))
