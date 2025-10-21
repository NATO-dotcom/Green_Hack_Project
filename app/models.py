from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    language = Column(String, default="en")
    alert_types = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
