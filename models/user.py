from sqlalchemy import Column, Integer, ARRAY, String, Boolean, DateTime, Date, Table
from db.base_class import Base
from sqlalchemy.orm import relationship


# user_roles = Table('user_roles', Base.metadata,
#                    Column('user_id', ForeignKey('user.id'), primary_key=True),
#                    Column('role_id', ForeignKey('roles.id'), primary_key=True)
#                    )


class User(Base):
    id = Column(Integer, primary_key=True)
    first_name = Column((String(32)), nullable=False)
    last_name = Column((String(32)), nullable=True)
    email = Column((String(256)), unique=True, nullable=False)
    phone = Column((String(15)), nullable=True)
    created_by = Column(Integer, nullable=True)
    modified_by = Column(Integer, nullable=True)
    skill = Column(ARRAY(String), nullable=True)
    addr = Column((String(256)), nullable=False)
    city = Column((String(32)), nullable=False)
    state = Column((String(32)), nullable=False)
    document_id = Column(Integer, nullable=True)
    english_proficiency = Column(Integer, nullable=False)
    last_education= Column((String(32)), nullable=False)

    # roles = relationship("Roles", secondary="user_roles",
    #                      back_populates="user")

    # subscriber_id = Column(
    #     Integer,
    #     ForeignKey('subscriber.id'),nullable=True,
    # )
