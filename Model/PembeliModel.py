from sqlalchemy import Column, Integer, String, ForeignKey
from conn import Base
from sqlalchemy.orm import relationship

class Pembeli(Base):
    __tablename__ = "pembeli"

    id_pembeli = Column(Integer, primary_key=True, autoincrement=True)
    id_users = Column(Integer, ForeignKey("users.id_users"), nullable=False)

    nama = Column(String(100))
    no_telp = Column(String(20))
    kecamatan = Column(String(100))
    alamat = Column(String(100))
    kodepos = Column(String(100))
    tgl_lahir = Column(String(50))
    jk = Column(String(100))
    email = Column(String(100))
    username = Column(String(50))
    password = Column(String(100))
    tgl_create = Column(String(20))

    user = relationship("User", back_populates="pembeli")
