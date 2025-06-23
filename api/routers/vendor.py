from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import models
import schemas
from core.database import get_db

router = APIRouter()


@router.post('/new_vendor')
def add_vendor(request: schemas.Vendor, db: Session = Depends(get_db)):
    vendor_exists = db.query(models.Vendor).filter(models.Vendor.email == request.email).first()
    if vendor_exists:
        raise HTTPException(status_code=400, detail="Vendor already exists")
    vendor = models.Vendor(vendor_name=request.vendor_name, brand_name=request.brand_name,
                           email=request.email, contact=request.contact, created_at=request.created_at)
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
