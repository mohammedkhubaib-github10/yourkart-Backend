from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import models
import schemas
from core.database import get_db

router = APIRouter()


@router.post('/add_product/{vendor_id}')
def add_product(vendor_id: str, request: schemas.Product, db: Session = Depends(get_db)):
    product = models.Product(product_name=request.product_name, product_image=request.product_image,
                             price=request.price, vendor_id=vendor_id, created_at=request.created_at)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get('/get_product/{vendor_id}')
def get_product(vendor_id: str, db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.vendor_id == vendor_id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No Products from this vendor")
    return products


@router.get('/get_all_product')
def get_all_product(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No Products available")
    return products


@router.put('/update_product/{product_id}/{vendor_id}')
def update_product(product_id: str, vendor_id: str, request: schemas.Product, db: Session = Depends(get_db)):
    product_query = db.query(models.Product).filter(models.Product.product_id == product_id,
                                                    models.Product.vendor_id == vendor_id)
    product = product_query.first()
    if not product:
        raise HTTPException(status_code=404, detail="No such Product")
    product_query.update(request.model_dump())
    db.commit()
    db.refresh(product)
    return product


@router.delete('/delete_product/{product_id}/{vendor_id}')
def delete_product(product_id: str, vendor_id: str, db: Session = Depends(get_db)):
    product_query = db.query(models.Product).filter(models.Product.product_id == product_id,
                                                    models.Product.vendor_id == vendor_id)
    product = product_query.first()
    if not product:
        raise HTTPException(status_code=404, detail="No such Product")
    db.delete(product)
    db.commit()
    return 'successful'
