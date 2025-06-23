from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import models
import schemas
from core.database import get_db

router = APIRouter()


@router.post('/new_customer')
def add_customer(request: schemas.Customer, db: Session = Depends(get_db)):
    customer_exists = db.query(models.Customer).filter(models.Customer.email == request.email).first()
    if customer_exists:
        raise HTTPException(status_code=400, detail="Customer already exists")
    customer = models.Customer(customer_name=request.customer_name,
                               email=request.email, contact=request.contact, created_at=request.created_at)
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
