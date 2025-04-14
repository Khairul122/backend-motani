from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from conn import Base

class LogStok(Base):
    __tablename__ = "log_stok"

    id_log = Column(Integer, primary_key=True, autoincrement=True)
    id_produk = Column(Integer, ForeignKey("produk.id_produk"), nullable=False)
    aksi = Column(String(50), nullable=False)
    perubahan = Column(Integer, nullable=False)
    tanggal_log = Column(DateTime(timezone=True), server_default=func.now())
