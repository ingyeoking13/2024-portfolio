import uuid
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TaskJob(Base):
    __tablename__ = 'TaskJob'
    id: Mapped[str] = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] =  Column(String(36), index=True)
    domain: Mapped[str] = Column(String(36), index=True)
    sub_domain: Mapped[str] = Column(String(36))
    parent_name: Mapped[str] =  Column(String(36), index=True)
    start_time: Mapped[datetime] = Column(DateTime)
    end_time: Mapped[datetime] = Column(DateTime)
    type: Mapped[str] = Column(String(32))
    result: Mapped[dict] = Column(JSON)
