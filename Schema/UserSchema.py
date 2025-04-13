from pydantic import BaseModel, EmailStr
from typing import Optional

# Response schema
class UserSchema(BaseModel):
    id_users: int
    nama: str
    email: EmailStr
    username: str
    password: str

    model_config = {
        "from_attributes": True
    }

# Schema untuk create user (POST)
class UserCreateSchema(BaseModel):
    nama: str
    email: EmailStr
    username: str
    password: str

    model_config = {
        "from_attributes": True
    }

# Schema untuk update user (PUT)
class UserUpdateSchema(BaseModel):
    nama: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
