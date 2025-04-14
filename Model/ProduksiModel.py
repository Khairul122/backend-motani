from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from conn import Base

class Produksi(Base):
    __tablename__ = "produksi"
    id_produksi = Column(Integer, primary_key=True, autoincrement=True)
    id_produk = Column(Integer, ForeignKey("produk.id_produk", ondelete="CASCADE"), nullable=False)
    tanggal_panen = Column(Date)
    tanggal_roasting = Column(Date)
    jumlah = Column(Integer, default=0)
    jenis_varietas = Column(String(100))
    nama_pemasok = Column(String(100))
    catatan = Column(Text)
    status_produksi = Column(String(30))

    produk = relationship("Produk", back_populates="produksi_items")
