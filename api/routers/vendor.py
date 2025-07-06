import random

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime
import models
import schemas
from core.database import get_db
from services.helper import save_otp, send_sms, verify

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
    vendor = db.query(models.Vendor).filter(models.Vendor.contact == contact).first()
    if not vendor:
        add_vendor(contact, db)
    return "logged in Successfully"


def add_vendor(contact: str, db: Session):
    vendor = models.Vendor(contact=contact, created_at=datetime.utcnow())
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


@router.get('/get_vendor/{vendor_id}')
def get_vendor(vendor_id: str, db: Session = Depends(get_db)):
    vendor = db.query(models.Vendor).filter(models.Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@router.get('/all_vendors')
def get_all_vendors(db: Session = Depends(get_db)):
    vendors = db.query(models.Vendor).all()
    return vendors


@router.put('/update_vendor/{vendor_id}')
def update_vendor(vendor_id: str, request: schemas.Vendor, db: Session = Depends(get_db)):
    vendor_query = db.query(models.Vendor).filter(models.Vendor.vendor_id == vendor_id)
    vendor = vendor_query.first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    vendor_query.update(request.model_dump())
    db.commit()
    db.refresh(vendor)
    return vendor


@router.delete('/delete_vendor/{vendor_id}')
def delete_vendor(vendor_id: str, db: Session = Depends(get_db)):
    vendor_query = db.query(models.Vendor).filter(models.Vendor.vendor_id == vendor_id)
    vendor = vendor_query.first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    db.delete(vendor)
    db.commit()
    return 'successfully deleted'
