from fastapi import FastAPI

from controller.router import customer, vendor, customer_address, vendor_address, cart, order, product
from infrastructure.database.session import Base
from infrastructure.database.session import engine

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(customer.router, prefix="/customer", tags=["Customer"])
app.include_router(vendor.router, prefix="/vendor", tags=["Vendor"])
app.include_router(product.router, prefix="/product", tags=["Product"])
app.include_router(customer_address.router, prefix="/customer_address", tags=["Customer Address"])
app.include_router(vendor_address.router, prefix="/vendor_address", tags=["Vendor Address"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])
app.include_router(order.router, prefix="/order", tags=["Order"])
