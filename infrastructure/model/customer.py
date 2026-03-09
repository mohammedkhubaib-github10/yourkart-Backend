import uuid

from sqlalchemy import Column, String, DATETIME
from sqlalchemy.orm import relationship

from infrastructure.database.session import Base


class Customer(Base):
    __tablename__ = 'Customers'
    customer_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_name = Column(String(100), )
    email = Column(String(100), unique=True)
    contact = Column(String(10), unique=True, nullable=False)
    created_at = Column(DATETIME, nullable=False)

    addresses = relationship('CustomerAddress', back_populates='customer', cascade='all, delete-orphan')
    cart = relationship('Cart', back_populates='customer', cascade='all, delete-orphan', uselist=False)
    orders = relationship('Order', back_populates='customer', cascade='all, delete-orphan')
