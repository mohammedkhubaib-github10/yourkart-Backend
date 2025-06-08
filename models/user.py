from core.database import SessionLocal, Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from address_table_secondary import address_table


class User(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    email = Column(String(20))
    contact = Column(String(10))

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

session = SessionLocal()
user_data = User(
    name='muaz',
    email='muaz10@gmail.com',
    contact='9400327485'
)
address1 = Address(
    street='merit',
    pincode='635810',
    city='pernambut',
    flat_no='32A',
)


result = session.query(User).filter(User.user_id == 2).first()
if result:
    session.delete(result)
    session.commit()
