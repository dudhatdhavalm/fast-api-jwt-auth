from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from datetime import datetime
from db.base_class import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column((String(120)), nullable=False)
    email = Column((String(120)), unique=True, nullable=False)
    password = Column((String(255)), nullable=False)
    is_super_admin = Column(Boolean, nullable=False, default=False)
    expiry_date = Column(Date, nullable=False)
    created_by = Column(Integer, nullable=True)
    modified_by = Column(Integer, nullable=True)
