from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from conn import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class KonsumenInDB(Base):
    __tablename__ = 'tb_konsumen'
    id = Column(Integer, primary_key=True, index=True)
    no_telp = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    nama = Column(String(100))
    token = Column(String(100), nullable=True)

class LogistikInDB(Base):
    __tablename__ = 'tb_logistik'
    id = Column(Integer, primary_key=True, index=True)
    no_hp = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    nama_toko = Column(String(100))

class User(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class RegistrasiKonsumen(BaseModel):
    nama: str
    no_telp: str
    alamat: str
    tgl_lahir: str
    jk: str
    email: str

    class Config:
        orm_mode = True

class RegistrasiLogistik(BaseModel):
    no_hp: str
    password: str
    nama_toko: str
    alamat: str
    lat: float
    lng: float
    status: str

    class Config:
        orm_mode = True

class LoginModel:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_konsumen(self, user: User):
        db_user = self.db.query(KonsumenInDB).filter(KonsumenInDB.no_telp == user.username).first()
        if db_user and db_user.password == user.password:
            return db_user
        return None

    def authenticate_logistik(self, user: User):
        db_user = self.db.query(LogistikInDB).filter(LogistikInDB.no_hp == user.username).first()
        if db_user and db_user.password == user.password:
            return db_user
        return None

    def registrasi_konsumen(self, params: dict):
        new_konsumen = KonsumenInDB(**params)
        self.db.add(new_konsumen)
        self.db.commit()
        return new_konsumen

    def registrasi_logistik(self, params: dict):
        new_logistik = LogistikInDB(**params)
        self.db.add(new_logistik)
        self.db.commit()
        return new_logistik

Base.metadata.create_all(bind=engine)
