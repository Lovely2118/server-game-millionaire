from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.utils import get_database_url

DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
