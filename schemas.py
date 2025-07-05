from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User schemas for API requests and responses

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None

class UserInfo(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


# Thread schemas for API requests and responses

class ThreadBase(BaseModel):
    title: str
    content: str

class ThreadCreate(ThreadBase):
    pass

class ThreadUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]

class ThreadList(ThreadBase):
    id: int

    class Config:
        orm_mode = True

class ThreadInfo(ThreadBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
