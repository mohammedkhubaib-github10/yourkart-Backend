from sqlalchemy import Table, Column, Integer, ForeignKey, String
from core.database import Base

address_table = Table(
    'user_address',
    Base.metadata,
    Column('customer_id', String(36), ForeignKey('Customers.customer_id')),
    Column('address_id', String(36), ForeignKey('Addresses.address_id'))
)
