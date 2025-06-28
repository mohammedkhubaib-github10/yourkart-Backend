import uuid

from sqlalchemy import Column, String, Float, DATETIME, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class Product(Base):
    __tablename__ = 'Products'
    product_id = Column(String(36), primary_key=True, default= lambda: str(uuid.uuid4()))
    product_name = Column(String(100), nullable=False)
    product_image = Column(String(100))
    price = Column(Float, nullable=False)
    vendor_id = Column(String(36), ForeignKey('Vendors.vendor_id'), nullable=False)
    created_at = Column(DATETIME, nullable=False)

    vendor = relationship('Vendor', back_populates='products')
    cart_items = relationship('CartItem', back_populates='product', cascade='all, delete-orphan')
