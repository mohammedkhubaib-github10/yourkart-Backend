from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from core.database import SessionLocal, engine
from schemas import Customer, Vendor

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
    customers = db.query(models.Customer).filter().all()
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
    db.delete(customer_query.first())
    db.commit()
    return 'successfull'


@app.post('/new_vendor')
def add_vendor(request: Vendor, db: Session = Depends(get_db)):
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
    vendors = db.query(models.Vendor).filter().all()
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
    db.delete(vendor_query.first())
    db.commit()
    return 'successfull'


