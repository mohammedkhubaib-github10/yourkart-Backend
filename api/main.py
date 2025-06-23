from fastapi import FastAPI

import models
from api.routers import customer, vendor, address, cart, order,product
from core.database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(customer.router, prefix="/customer", tags=["Customer"])
app.include_router(vendor.router, prefix="/vendor", tags=["Vendor"])
app.include_router(product.router, prefix="/product", tags=["Product"])
app.include_router(address.router, prefix="/address", tags=["Address"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])
app.include_router(order.router, prefix="/order", tags=["Order"])
