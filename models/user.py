from core.database import SessionLocal, Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import relationship
from address_user_link import address_table


class Customer(Base):
    __tablename__ = 'Customers'
    customer_id = Column(String(36), primary_key=True)
    name = Column(String(20), nullable=False)
    email = Column(String(20), unique=True)
    contact = Column(String(10), unique=True)

    addresses = relationship('Address', secondary=address_table, back_populates='customers')
    cart = relationship('Cart', back_populates='customer', cascade='all, delete-orphan', uselist=False)
    orders = relationship('Order', back_populates='customer', cascade = 'all, delete-orphan')


class Address(Base):
    __tablename__ = 'Addresses'
    address_id = Column(String(36), primary_key=True)
    street = Column(String(20))
    pincode = Column(String(10), nullable=False)
    city = Column(String(20))
    flat_no = Column(String(5))
    location = Column(String(50), nullable=False)
    vendor_id = Column(String(36), ForeignKey('Vendors.vendor_id'), nullable=False)

    customers = relationship('Customer', secondary=address_table, back_populates='addresses')

    vendor = relationship('Vendor', back_populates= 'shop_addresses')


class Vendor(Base):
    __tablename__ = 'Vendors'
    vendor_id = Column(String(36), primary_key=True)
    brand_name = Column(String(20), unique=True, nullable=False)

    shop_addresses = relationship('Address', back_populates='vendor', cascade= 'all, delete-orphan')
    products = relationship('Product', back_populates='vendor', cascade='all, delete-orphan')


class Product(Base):
    __tablename__ = 'Products'
    product_id = Column(String(36), primary_key=True)
    product_name = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    vendor_id = Column(String(36), ForeignKey('Vendors.vendor_id'), nullable=False)

    vendor = relationship('Vendor', back_populates='products')
    cart_items = relationship('CartItem', back_populates='product', cascade='all, delete-orphan')


class Cart(Base):
    __tablename__ = 'Carts'
    cart_id = Column(String(36), primary_key=True)
    customer_id = Column(String(36), ForeignKey('Customers.customer_id'), nullable=False)

    customer = relationship('Customer', back_populates= 'cart', uselist=False)
    items = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')
    order = relationship('Order', back_populates='cart', uselist= False)


class CartItem(Base):
    __tablename__ = 'Cart_Items'
    item_id = Column(String(36), primary_key=True)
    qty = Column(Integer, nullable=False, default= 1)
    total_price = Column(Float, nullable=False)
    cart_id = Column(String(36), ForeignKey('Carts.cart_id'), nullable=False)
    product_id = Column(String(36), ForeignKey('Products.product_id'), nullable=False)

    product = relationship('Product', back_populates='cart_items')
    cart = relationship('Cart', back_populates='items')


class Order(Base):
    __tablename__ = 'Orders'
    order_id = Column(String(36), primary_key=True)
    total_price = Column(Float, nullable=False)
    order_status = Column(String(20), nullable=False)
    customer_id = Column(String(36), ForeignKey('Customers.customer_id'), nullable=False)
    cart_id = Column(String(36), ForeignKey('Carts.cart_id'), nullable=False)

    customer = relationship('Customer', back_populates='orders')
    cart = relationship('Cart', back_populates='order', uselist= False)
    payment = relationship('Payment', back_populates='order', uselist=False)


class Payment(Base):
    __tablename__ = 'Payments'
    payment_id = Column(String(36), primary_key=True)
    payment_mode = Column(String(20), nullable=False)
    payment_amount = Column(Float, nullable=False)
    payment_status = Column(String(10), nullable=False)
    order_id = Column(String(36), ForeignKey('Orders.order_id'), nullable=False)

    order = relationship('Order', back_populates='payment', uselist=False)


Base.metadata.create_all(engine)

