from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from core.database import SessionLocal, engine
from schemas import Customer, Vendor, VendorAddress, CustomerAddress, Product

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


@app.post('/new_customer')
def add_customer(request: Customer, db: Session = Depends(get_db)):
    customer_exists = db.query(models.Customer).filter(models.Customer.email == request.email).first()
    if customer_exists:
        raise HTTPException(status_code=400, detail="Customer already exists")
    customer = models.Customer(customer_name=request.customer_name,
                               email=request.email, contact=request.contact, created_at=request.created_at)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@app.get('/get_customer/{customer_id}')
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.get('/all_customers')
def get_all_customers(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return customers


@app.put('/update_customer/{customer_id}')
def update_customer(customer_id: str, request: Customer, db: Session = Depends(get_db)):
    customer_query = db.query(models.Customer).filter(models.Customer.customer_id == customer_id)
    customer = customer_query.first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer_query.update(request.model_dump())
    db.commit()
    db.refresh(customer)
    return customer


@app.delete('/delete_customer/{customer_id}')
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    customer_query = db.query(models.Customer).filter(models.Customer.customer_id == customer_id)
    customer = customer_query.first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return 'successfull'


@app.post('/new_vendor')
def add_vendor(request: Vendor, db: Session = Depends(get_db)):
    vendor_exists = db.query(models.Vendor).filter(models.Vendor.email == request.email).first()
    if vendor_exists:
        raise HTTPException(status_code=400, detail="Vendor already exists")
    vendor = models.Vendor(vendor_name=request.vendor_name, brand_name=request.brand_name,
                           email=request.email, contact=request.contact, created_at=request.created_at)
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


@app.get('/get_vendor/{vendor_id}')
def get_vendor(vendor_id: str, db: Session = Depends(get_db)):
    vendor = db.query(models.Vendor).filter(models.Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@app.get('/all_vendors')
def get_all_vendors(db: Session = Depends(get_db)):
    vendors = db.query(models.Vendor).all()
    return vendors


@app.put('/update_vendor/{vendor_id}')
def update_vendor(vendor_id: str, request: Vendor, db: Session = Depends(get_db)):
    vendor_query = db.query(models.Vendor).filter(models.Vendor.vendor_id == vendor_id)
    vendor = vendor_query.first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    vendor_query.update(request.model_dump())
    db.commit()
    db.refresh(vendor)
    return vendor


@app.delete('/delete_vendor/{vendor_id}')
def delete_vendor(vendor_id: str, db: Session = Depends(get_db)):
    vendor_query = db.query(models.Vendor).filter(models.Vendor.vendor_id == vendor_id)
    vendor = vendor_query.first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    db.delete(vendor)
    db.commit()
    return 'successfull'


@app.post('/new_vendoraddress/{vendor_id}')
def add_address(vendor_id: str, request: VendorAddress, db: Session = Depends(get_db)):
    address = models.VendorAddress(street=request.street, pincode=request.pincode,
                                   city=request.city, location=request.location,
                                   vendor_id=vendor_id)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@app.get('/get_vendor_addresses/{vendor_id}')
def get_address(vendor_id: str, db: Session = Depends(get_db)):
    address = db.query(models.VendorAddress).filter(models.VendorAddress.vendor_id == vendor_id).all()
    return address


@app.put('/update_vendor_address/{vendor_id}/{address_id}')
def update_address(vendor_id: str, address_id: str, request: VendorAddress, db: Session = Depends(get_db)):
    address_query = db.query(models.VendorAddress).filter(models.VendorAddress.address_id == address_id,
                                                          models.VendorAddress.vendor_id == vendor_id)
    address = address_query.first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    address_query.update(request.model_dump())
    db.commit()
    db.refresh(address)
    return address


@app.delete('/delete_vendor_address/{vendor_id}/{address_id}')
def delete_address(vendor_id: str, address_id: str, db: Session = Depends(get_db)):
    address_query = db.query(models.VendorAddress).filter(models.VendorAddress.address_id == address_id,
                                                          models.VendorAddress.vendor_id == vendor_id)
    address = address_query.first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    return 'Successful'


@app.post('/new_customer_address/{customer_id}')
def add_address(customer_id: str, request: CustomerAddress, db: Session = Depends(get_db)):
    address = models.CustomerAddress(street=request.street, pincode=request.pincode,
                                     city=request.city, flat_no=request.flat_no, location=request.location,
                                     customer_id=customer_id)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@app.get('/get_customer_addresses/{customer_id}')
def get_address(customer_id: str, db: Session = Depends(get_db)):
    address = db.query(models.CustomerAddress).filter(models.CustomerAddress.customer_id == customer_id).all()
    return address


@app.put('/update_customer_address/{customer_id}/{address_id}')
def update_address(customer_id: str, address_id: str, request: CustomerAddress, db: Session = Depends(get_db)):
    address_query = db.query(models.CustomerAddress).filter(models.CustomerAddress.address_id == address_id,
                                                            models.CustomerAddress.customer_id == customer_id)
    address = address_query.first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    address_query.update(request.model_dump())
    db.commit()
    db.refresh(address)
    return address


@app.delete('/delete_customer_address/{customer_id}/{address_id}')
def delete_address(customer_id: str, address_id: str, db: Session = Depends(get_db)):
    address_query = db.query(models.CustomerAddress).filter(models.CustomerAddress.address_id == address_id,
                                                            models.CustomerAddress.customer_id == customer_id)
    address = address_query.first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    return 'Successful'


@app.post('/add_product/{vendor_id}')
def add_product(vendor_id: str, request: Product, db: Session = Depends(get_db)):
    product = models.Product(product_name=request.product_name, product_image=request.product_image,
                             price=request.price, vendor_id=vendor_id, created_at=request.created_at)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.get('/get_product/{vendor_id}')
def get_product(vendor_id: str, db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.vendor_id == vendor_id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No Products from this vendor")
    return products


@app.get('/get_all_product')
def get_all_product(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No Products available")
    return products


@app.put('/update_product/{product_id}/{vendor_id}')
def update_product(product_id: str, vendor_id: str, request: Product, db: Session = Depends(get_db)):
    product_query = db.query(models.Product).filter(models.Product.product_id == product_id,
                                                    models.Product.vendor_id == vendor_id)
    product = product_query.first()
    if not product:
        raise HTTPException(status_code=404, detail="No such Product")
    product_query.update(request.model_dump())
    db.commit()
    db.refresh(product)
    return product


@app.delete('/delete_product/{product_id}/{vendor_id}')
def delete_product(product_id: str, vendor_id: str, db: Session = Depends(get_db)):
    product_query = db.query(models.Product).filter(models.Product.product_id == product_id,
                                                    models.Product.vendor_id == vendor_id)
    product = product_query.first()
    if not product:
        raise HTTPException(status_code=404, detail="No such Product")
    db.delete(product)
    db.commit()
    return 'successful'


@app.post('/add_cart/{customer_id}')
def add_cart(customer_id: str, db: Session = Depends(get_db)):
    existing_cart = db.query(models.Cart).filter(models.Cart.customer_id == customer_id).first()
    if existing_cart:
        raise HTTPException(status_code=400, detail="Already Cart Exists")
    cart = models.Cart(customer_id=customer_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


@app.get('/view_cart_items/{cart_id}')
def view_items(cart_id: str, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.cart_id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart does not exists")
    cart_items = db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id).all()
    items = []
    for item in cart_items:
        product = db.query(models.Product).filter(models.Product.product_id == item.product_id).first()
        items.append({
            "item_id": item.item_id,
            "product_id": item.product_id,
            "product_name": product.product_name if product else "Unknown",
            "product_image": product.product_image if product else None,
            "qty": item.qty,
            "price_per_unit": product.price if product else None,
            "total_price": item.total_price
        })

    return {
        "cart_id": cart.cart_id,
        "customer_id": cart.customer_id,
        "total_amount": cart.amount,
        "items": items
    }


def update_cart_amount(cart_id: str, item_price: float, db: Session, add: bool):
    cart = db.query(models.Cart).filter(models.Cart.cart_id == cart_id).first()
    if cart:
        if add:
            cart.amount += item_price
        else:
            cart.amount = max(0, cart.amount - item_price)

        db.commit()


@app.post('/add_items/{cart_id}/{product_id}')
def add_items(cart_id: str, product_id: str, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.cart_id == cart_id).first()
    existing_items = db.query(models.CartItem, models.Product).join(models.Product,
                                                models.CartItem.product_id == models.Product.product_id).filter(
        models.CartItem.cart_id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart doesn't Exist")

    item_query = db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id,
                                                  models.CartItem.product_id == product_id)
    item = item_query.first()
    product_query = db.query(models.Product).filter(models.Product.product_id == product_id)
    product = product_query.first()
    if existing_items:
        if existing_items.Product.vendor_id != product.vendor_id:
            raise HTTPException(status_code=400, detail="Cannot add products of a different vendor")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if item:
        item.qty += 1
        item.total_price = product.price * item.qty
    else:
        item = models.CartItem(
            cart_id=cart_id, product_id=product_id, total_price=product.price
        )
        db.add(item)

    db.commit()
    db.refresh(item)

    update_cart_amount(cart_id, product.price, db, True)
    return item


@app.delete('/delete_items/{cart_id}/{item_id}')
def delete_item(item_id: str, cart_id: str, db: Session = Depends(get_db)):
    item_query = db.query(models.CartItem).filter(models.CartItem.item_id == item_id,
                                                  models.CartItem.cart_id == cart_id)
    item = item_query.first()
    if not item:
        raise HTTPException(status_code=404, detail="Item does not exist")
    item_price = item.total_price / item.qty
    if item.qty == 1:
        db.delete(item)
    else:
        item.qty -= 1
        item.total_price = item.qty * item_price
    db.commit()

    update_cart_amount(cart_id, item_price, db, False)
    return "successful"


@app.post('/place_order/{cart_id}')
def place_order(cart_id: str, request: schemas.Order, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.cart_id == cart_id).first()
    items_query = db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id)
    items = items_query.all()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart Not Found")
    if cart.amount == 0:
        raise HTTPException(status_code=404, detail="Empty Cart")

    order = models.Order(total_price=cart.amount, customer_id=cart.customer_id, cart_id=cart.cart_id,
                         order_status=request.order_status, delivery_address_id=request.delivery_address_id,
                         created_at=request.created_at)
    db.add(order)
    db.commit()
    db.refresh(order)
    for item in items:
        order_item = models.OrderItem(
            order_id=order.order_id,
            product_id=item.product_id,
            qty=item.qty,
            total_price=item.total_price
        )
        db.add(order_item)
    items_query.delete(synchronize_session=False)
    cart.amount = 0
    db.commit()
    return order


@app.delete('/delete_order/{order_id}')
def delete_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order does not exist")
    db.delete(order)
    db.commit()
    return 'Successful'


@app.get('/get_customer_orders/{customer_id}')
def get_customer_orders(customer_id: str, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No Orders Found")

    result = []
    for order in orders:
        items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order.order_id).all()
        result.append({
            "order_id": order.order_id,
            "total_price": order.total_price,
            "status": order.order_status,
            "created_at": order.created_at,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": db.query(models.Product).filter(
                        models.Product.product_id == item.product_id).first().product_name,
                    "qty": item.qty,
                    "total_price": item.total_price
                } for item in items
            ]
        })

    return result


@app.get('/get_vendor_orders/{vendor_id}')
def get_vendor_orders(vendor_id: str, db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Order.order_id,
            models.Order.total_price,
            models.Order.created_at,
            models.Customer.customer_name,
            models.Customer.contact,
            models.CustomerAddress.street,
            models.CustomerAddress.city,
            models.CustomerAddress.pincode,
            models.CustomerAddress.flat_no,
            models.Product.product_name,
            models.OrderItem.qty,
            models.OrderItem.total_price
        )
        .join(models.OrderItem, models.Order.order_id == models.OrderItem.order_id)
        .join(models.Product, models.OrderItem.product_id == models.Product.product_id)
        .join(models.Customer, models.Order.customer_id == models.Customer.customer_id)
        .join(models.CustomerAddress, models.Order.delivery_address_id == models.CustomerAddress.address_id)
        .filter(models.Product.vendor_id == vendor_id, models.Order.order_status == "OrderStatus.Placed")
        .all()
    )
    response = []
    for row in results:
        response.append({
            "order_id": row[0],
            "total_price": row[1],
            "created_at": row[2],
            "customer_name": row[3],
            "customer_contact": row[4],
            "customer_street": row[5],
            "customer_city": row[6],
            "customer_pincode": row[7],
            "customer_flat_no": row[8],
            "product_name": row[9],
            "qty": row[10],
            "item_total_price": row[11]
        })
        if not response:
            raise HTTPException(status_code=400, detail="No Orders Found")
    return response
