from core.database import SessionLocal, Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from address_user_link import address_table


class Customer(Base):
    __tablename__ = 'Customers'
    customer_id = Column(String(36), primary_key=True)
    name = Column(String(20), nullable=False)
    email = Column(String(20))
    contact = Column(String(10))

    addresses = relationship('Address', secondary=address_table, back_populates='customers')


class Address(Base):
    __tablename__ = 'Addresses'
    address_id = Column(String(36), primary_key=True)
    street = Column(String(20))
    pincode = Column(String(10), nullable=False)
    city = Column(String(20))
    flat_no = Column(String(5))
    location = Column(String(50))
    vendor_id = Column(String(36), ForeignKey('Vendors.vendor_id'))

    customers = relationship('Customer', secondary=address_table, back_populates='addresses')

    vendor = relationship('Vendor', back_populates= 'shop_addresses')


class Vendor(Base):
    __tablename__ = 'Vendors'
    vendor_id = Column(String(36), primary_key=True)
    brand_name = Column(String(20), unique=True)

    shop_addresses = relationship('Address', back_populates='vendor')


Base.metadata.create_all(engine)

