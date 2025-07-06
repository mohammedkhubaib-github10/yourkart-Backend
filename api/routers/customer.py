import random
from datetime import datetime

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import models
import schemas
from core.database import get_db
from services.helper import verify, send_sms, save_otp

router = APIRouter()


@router.post('/request_otp')
def request_otp(contact: str):
    otp = str(random.randint(10000, 99999))
    save_otp(contact, otp)
    send_sms(contact, otp)
    return "OTP Sent Successfully " + otp


@router.post('/verify_otp')
def verify_otp(contact: str, customer_otp: str, db: Session = Depends(get_db)):
    result = verify(contact, customer_otp)
    if not result:
        raise HTTPException(detail="Invalid OTP or Time out", status_code=404)
    customer = db.query(models.Customer).filter(models.Customer.contact == contact).first()
    if not customer:
        add_customer(contact, db)
    return "logged in Successfully"


def add_customer(contact: str, db: Session):
    customer = models.Customer(contact=contact, created_at=datetime.utcnow())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get('/get_customer/{customer_id}')
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get('/all_customers')
def get_all_customers(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return customers


@router.put('/update_customer/{customer_id}')
def update_customer(customer_id: str, request: schemas.Customer, db: Session = Depends(get_db)):
    customer_query = db.query(models.Customer).filter(models.Customer.customer_id == customer_id)
    customer = customer_query.first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer_query.update(request.model_dump())
    db.commit()
    db.refresh(customer)
    return customer


@router.delete('/delete_customer/{customer_id}')
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    customer_query = db.query(models.Customer).filter(models.Customer.customer_id == customer_id)
    customer = customer_query.first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return 'successfully deleted'
