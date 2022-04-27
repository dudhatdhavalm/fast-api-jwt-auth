from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from datetime import datetime
from db.database import DBBaseModel

class UserModel(DBBaseModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column((String(120)), nullable=False)
    email = Column((String(120)), unique=True, nullable=False)
    password = Column((String(255)), nullable=False)
    inserted_date = Column(DateTime, nullable=False,
      default=(datetime.utcnow))
    is_active = Column(Boolean, nullable=False, default=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_block = Column(Boolean, nullable=False, default=False)
    expiry_date = Column(Date, nullable=False)