from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from infrastructure import model
from controller import schema
from infrastructure.database.session import get_db
from service.helper import haversine

router = APIRouter()


@router.post('/add_product/{vendor_id}')
def add_product(vendor_id: str, request: schema.Product, db: Session = Depends(get_db)):
    product = model.Product(product_name=request.product_name, product_image=request.product_image,
                            price=request.price, vendor_id=vendor_id, created_at=request.created_at)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get('/get_product/{vendor_id}')
def get_product(vendor_id: str, db: Session = Depends(get_db)):
    products = db.query(model.Product).filter(model.Product.vendor_id == vendor_id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No Products from this vendor")
    return products


@router.get('/get_all_product')
def get_all_product(db: Session = Depends(get_db)):
    products = db.query(model.Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No Products available")
    return products


# needs rewrite
@router.get('/get_nearby_products/{address_id}')
def get_nearby_products(address_id: str, db: Session = Depends(get_db)):
    customer_address = db.query(model.CustomerAddress).filter(model.CustomerAddress.address_id == address_id).first()
    if not customer_address:
        raise HTTPException(status_code=404, detail="No such Address")
    customer_latitude = customer_address.latitude
    customer_longitude = customer_address.longitude
    vendors = db.query(model.VendorAddress).all()
    nearby_vendors = []
    for vendor in vendors:
        if vendor.latitude is None or vendor.longitude is None:
            continue
        distance = haversine(customer_latitude, customer_longitude, vendor.latitude, vendor.longitude)
        if distance < 5:
            nearby_vendors.append(vendor.vendor_id)
    if not nearby_vendors:
        raise HTTPException(status_code=404, detail="No nearby vendors found")
    nearby_products = db.query(model.Product).filter(model.Product.vendor_id.in_(nearby_vendors)).all()
    return nearby_products


@router.put('/update_product/{product_id}/{vendor_id}')
def update_product(product_id: str, vendor_id: str, request: schema.Product, db: Session = Depends(get_db)):
    product_query = db.query(model.Product).filter(model.Product.product_id == product_id,
                                                   model.Product.vendor_id == vendor_id)
    product = product_query.first()
    if not product:
        raise HTTPException(status_code=404, detail="No such Product")
    product_query.update(request.model_dump())
    db.commit()
    db.refresh(product)
    return product


@router.delete('/delete_product/{product_id}/{vendor_id}')
def delete_product(product_id: str, vendor_id: str, db: Session = Depends(get_db)):
    product_query = db.query(model.Product).filter(model.Product.product_id == product_id,
                                                   model.Product.vendor_id == vendor_id)
    product = product_query.first()
    if not product:
        raise HTTPException(status_code=404, detail="No such Product")
    db.delete(product)
    db.commit()
    return 'successful'
