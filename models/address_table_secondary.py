from sqlalchemy import Table, Column, Integer, ForeignKey
from core.database import Base

address_table = Table(
    'user_address',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('Users.user_id')),
    Column('address_id', Integer, ForeignKey('Addresses.address_id'))
)
