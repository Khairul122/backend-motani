from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from conn import Base

class KalenderPanen(Base):
    __tablename__ = "kalender_panen"
    __table_args__ = {'extend_existing': True}

    id_kalender = Column(Integer, primary_key=True, autoincrement=True)
    id_informasi = Column(Integer, ForeignKey("informasi.id_informasi"))
    wilayah = Column(String(100))
    awal_panen = Column(Date)
    akhir_panen = Column(Date)
    catatan = Column(Text)

    informasi = relationship("Informasi", backref="kalender_panen")
