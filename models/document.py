from sqlalchemy import Column, Integer, String , ForeignKey
from db.base_class import Base

class Document(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    static_file_path = Column(String(256), nullable=False)
    actual_file_path = Column(String(256), nullable=True)
    created_by = Column(
        Integer,
        ForeignKey('user.id'),nullable=True,
    )
    modified_by = Column(
        Integer,
        ForeignKey('user.id'),nullable=True,
    )