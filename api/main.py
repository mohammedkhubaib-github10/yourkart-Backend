from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from core.database import SessionLocal, engine
from schemas import Customer, Vendor, VendorAddress, CustomerAddress

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
    if not customer_query.first():
        raise HTTPException(status_code=404, detail="Customer not found")
    customer_query.update(request.model_dump())
    db.commit()
    return 'successfull'


@app.delete('/delete_customer/{customer_id}')
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    customer_query = db.query(models.Customer).filter(models.Customer.customer_id == customer_id)
    if not customer_query.first():
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer_query)
    db.commit()
    return 'successfull'


@app.post('/new_vendor')
def add_vendor(request: Vendor, db: Session = Depends(get_db)):
    vendor_exists = db.query(models.Vendor).filter(request.email).first()
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
    if not vendor_query.first():
        raise HTTPException(status_code=404, detail="Vendor not found")
    vendor_query.update(request.model_dump())
    db.commit()
    return 'successfull'


@app.delete('/delete_vendor/{vendor_id}')
def delete_vendor(vendor_id: str, db: Session = Depends(get_db)):
    vendor_query = db.query(models.Vendor).filter(models.Vendor.vendor_id == vendor_id)
    if not vendor_query.first():
        raise HTTPException(status_code=404, detail="Vendor not found")
    db.delete(vendor_query)
    db.commit()
    return 'successfull'


@app.post('/new_address/{vendor_id}')
def add_address(vendor_id: str, request: VendorAddress, db: Session = Depends(get_db)):
    address = models.VendorAddress(street=request.street, pincode=request.pincode,
                                   city=request.city, location=request.location,
                                   vendor_id=vendor_id)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@app.get('/get_addresses/{vendor_id}')
def get_address(vendor_id: str, db: Session = Depends(get_db)):
    address = db.query(models.VendorAddress).filter(models.VendorAddress.vendor_id == vendor_id).all()
    return address


@app.put('/update_address/{vendor_id}/{address_id}')
def update_address(vendor_id: str, address_id: str, request: VendorAddress, db: Session = Depends(get_db)):
    address_query = db.query(models.VendorAddress).filter(models.VendorAddress.address_id == address_id,
                                                          models.VendorAddress.vendor_id == vendor_id)
    if not address_query.first():
        raise HTTPException(status_code=404, detail="Address not found")
    address_query.update(request.model_dump())
    db.commit()
    return 'successfull'


@app.delete('/delete_address/{vendor_id}/{address_id}')
def delete_address(vendor_id: str, address_id: str, db: Session = Depends(get_db)):
    address_query = db.query(models.VendorAddress).filter(models.VendorAddress.address_id == address_id,
                                                          models.VendorAddress.vendor_id == vendor_id)
    if not address_query.first():
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address_query)
    db.commit()
    return 'Successful'


@app.post('/new_address/{customer_id}')
def add_address(customer_id: str, request: CustomerAddress, db: Session = Depends(get_db)):
    address = models.CustomerAddress(street=request.street, pincode=request.pincode,
                                     city=request.city, flat_no=request.flat_no, location=request.location,
                                     customer_id=customer_id)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@app.get('/get_addresses/{customer_id}')
def get_address(customer_id: str, db: Session = Depends(get_db)):
    address = db.query(models.CustomerAddress).filter(models.CustomerAddress.customer_id == customer_id).all()
    return address


@app.put('/update_address/{customer_id}/{address_id}')
def update_address(customer_id: str, address_id: str, request: CustomerAddress, db: Session = Depends(get_db)):
    address_query = db.query(models.CustomerAddress).filter(models.CustomerAddress.address_id == address_id,
                                                            models.CustomerAddress.customer_id == customer_id)
    if not address_query.first():
        raise HTTPException(status_code=404, detail="Address not found")
    address_query.update(request.model_dump())
    db.commit()
    return 'successfull'


@app.delete('/delete_address/{customer_id}/{address_id}')
def delete_address(customer_id: str, address_id: str, db: Session = Depends(get_db)):
    address_query = db.query(models.CustomerAddress).filter(models.CustomerAddress.address_id == address_id,
                                                            models.CustomerAddress.customer_id == customer_id)
    if not address_query.first():
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address_query)
    db.commit()
    return 'Successful'
