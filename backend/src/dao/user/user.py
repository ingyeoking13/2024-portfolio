import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id: Mapped[str] = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] =  Column(String(36), index=True)
    nickname: Mapped[str] =  Column(String(36), index=True)
    email: Mapped[str] = Column(String(64), index=True)
    password: Mapped[str] = Column(String(64))
    salt: Mapped[str] = Column(String(32))
