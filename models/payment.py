import uuid

from sqlalchemy import Column, String, Float, ForeignKey, DATETIME
from sqlalchemy.orm import relationship

from core.database import Base


class Payment(Base):
    __tablename__ = 'Payments'
    payment_id = Column(String(36), primary_key=True, default= lambda: str(uuid.uuid4()))
    payment_mode = Column(String(20), nullable=False)
    payment_amount = Column(Float, nullable=False)
    payment_status = Column(String(10), nullable=False)
    order_id = Column(String(36), ForeignKey('Orders.order_id'), nullable=False)
    payment_on = Column(DATETIME, nullable=False)

    order = relationship('Order', back_populates='payment', uselist=False)
