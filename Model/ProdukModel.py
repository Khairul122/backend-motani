from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from conn import Base

class Produk(Base):
    __tablename__ = "produk"
    id_produk = Column(Integer, primary_key=True, autoincrement=True)
    nama_produk = Column(String(255), nullable=False)
    keterangan = Column(Text)
    stok = Column(Integer, default=0)
    deskripsi = Column(Text)
    status_produk = Column(String(30), default="aktif")
    id_logistik = Column(Integer, ForeignKey("logistik.id"))
    harga = Column(DECIMAL(12, 2), nullable=False, default=0.00)
    diskon = Column(DECIMAL(5, 2), default=0.00)
    produksi_items = relationship("Produksi", back_populates="produk", cascade="all, delete")   
    produk_foto = relationship("ProdukFoto", back_populates="produk", cascade="all, delete")


class ProdukFoto(Base):
    __tablename__ = "produk_foto"
    id_foto = Column(Integer, primary_key=True, autoincrement=True)
    id_produk = Column(Integer, ForeignKey("produk.id_produk", ondelete="CASCADE"), nullable=False)
    url_foto = Column(String(500), nullable=False)

    produk = relationship("Produk", back_populates="produk_foto")
