from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_Url = "postgresql://yourkart_user:5rS66n1rzzqbZDgZhggO3R9dnae3faqW@dpg-d42vh8odl3ps73cr5uig-a/yourkart"

engine = create_engine(DB_Url)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
