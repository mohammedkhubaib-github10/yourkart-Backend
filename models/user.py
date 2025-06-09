from core.database import SessionLocal, Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from address_user_link import address_table


class User(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    email = Column(String(20))
    contact = Column(String(10))
    location = Column(String(50))

    address = relationship('Address', secondary=address_table, back_populates='user', cascade="all, delete")


class Address(Base):
    __tablename__ = 'Addresses'
    address_id = Column(Integer, primary_key=True)
    street = Column(String(20))
    pincode = Column(String(10), nullable=False)
    city = Column(String(20))
    flat_no = Column(String(5))

    user = relationship('User', secondary=address_table, back_populates='address')


Base.metadata.create_all(engine)

