from sqlalchemy import Column, Integer, String, Double, Enum, ForeignKey
from sqlalchemy.orm import relationship
from conn import Base
import enum

class StatusLogistik(str, enum.Enum):
    penjual = "penjual"
    roasting = "roasting"
    pengepul = "pengepul"

class Logistik(Base):
    __tablename__ = "logistik"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(100))
    no_hp = Column(String(50))
    alamat = Column(String(200))
    nama_toko = Column(String(100), nullable=True)
    lat = Column(Double)
    lng = Column(Double)
    id_users = Column(Integer, ForeignKey("users.id_users"), nullable=False)
    status = Column(Enum("penjual", "roasting", "pengepul"))

    user = relationship("User", back_populates="logistik")
