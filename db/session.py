from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.setting import setting


engine = create_engine(
    setting.SQLALCHEMY_DATABASE_URL
    # required for sqlite
    # connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
