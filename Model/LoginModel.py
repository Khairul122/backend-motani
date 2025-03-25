from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from pydantic import BaseModel
from conn import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserInDB(Base):
    __tablename__ = 'tb_administrator'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    nama = Column(String(100))

class User(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class LoginModel:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, user: User):
        db_user = self.db.query(UserInDB).filter(UserInDB.username == user.username).first()
        if db_user and db_user.password == user.password:
            return db_user
        return None

Base.metadata.create_all(bind=engine)
