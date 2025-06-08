from sqlalchemy import Column, Integer, String, Float

from core.database import Base


class Developer(Base):
    __tablename__ = "developers"
    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String(20))
    Exp = Column(Float)

