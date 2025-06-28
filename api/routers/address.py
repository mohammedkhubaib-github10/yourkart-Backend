from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import models
import schemas
from core.database import get_db

router = APIRouter()


@router.post('/new_vendor_address/{vendor_id}')
def add_address(vendor_id: str, request: schemas.VendorAddress, db: Session = Depends(get_db)):
    address = models.VendorAddress(street=request.street, pincode=request.pincode,
                                   city=request.city, latitude=request.latitude,
                                   longitude=request.longitude,
                                   vendor_id=vendor_id)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@router.get('/get_vendor_addresses/{vendor_id}')
def get_address(vendor_id: str, db: Session = Depends(get_db)):
    address = db.query(models.VendorAddress).filter(models.VendorAddress.vendor_id == vendor_id).all()
    return address


@router.put('/update_vendor_address/{vendor_id}/{address_id}')
def update_address(vendor_id: str, address_id: str, request: schemas.VendorAddress, db: Session = Depends(get_db)):
    address_query = db.query(models.VendorAddress).filter(models.VendorAddress.address_id == address_id,
                                                          models.VendorAddress.vendor_id == vendor_id)
    address = address_query.first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    address_query.update(request.model_dump())
    db.commit()
    db.refresh(address)
    return address


@router.delete('/delete_vendor_address/{vendor_id}/{address_id}')
def delete_address(vendor_id: str, address_id: str, db: Session = Depends(get_db)):
    address_query = db.query(models.VendorAddress).filter(models.VendorAddress.address_id == address_id,
                                                          models.VendorAddress.vendor_id == vendor_id)
    address = address_query.first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    return 'Successful'


@router.post('/new_customer_address/{customer_id}')
def add_address(customer_id: str, request: schemas.CustomerAddress, db: Session = Depends(get_db)):
    address = models.CustomerAddress(street=request.street, pincode=request.pincode,
                                     city=request.city, flat_no=request.flat_no, latitude=request.latitude,
                                     longitude=request.longitude,
                                     customer_id=customer_id)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@router.get('/get_customer_addresses/{customer_id}')
def get_address(customer_id: str, db: Session = Depends(get_db)):
    address = db.query(models.CustomerAddress).filter(models.CustomerAddress.customer_id == customer_id).all()
    return address


@router.put('/update_customer_address/{customer_id}/{address_id}')
def update_address(customer_id: str, address_id: str, request: schemas.CustomerAddress, db: Session = Depends(get_db)):
    address_query = db.query(models.CustomerAddress).filter(models.CustomerAddress.address_id == address_id,
                                                            models.CustomerAddress.customer_id == customer_id)
    address = address_query.first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    address_query.update(request.model_dump())
    db.commit()
    db.refresh(address)
    return address


@router.delete('/delete_customer_address/{customer_id}/{address_id}')
def delete_address(customer_id: str, address_id: str, db: Session = Depends(get_db)):
    address_query = db.query(models.CustomerAddress).filter(models.CustomerAddress.address_id == address_id,
                                                            models.CustomerAddress.customer_id == customer_id)
    address = address_query.first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    return 'Successful'
