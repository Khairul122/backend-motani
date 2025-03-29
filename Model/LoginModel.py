from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from conn import Base

class User(Base):
    __tablename__ = "users"

    id_users = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    level = Column(String(30), nullable=False)

    pembeli = relationship("Pembeli", back_populates="user", uselist=False)
    logistik = relationship("Logistik", back_populates="user", uselist=False)
