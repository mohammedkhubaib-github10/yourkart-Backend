from fastapi import Depends, HTTPException, APIRouter

from controller import schema
from controller.dependency.product_dependency import get_product_service
from domain.exception import ProductNotFound

router = APIRouter()


@router.post('/add_product/{vendor_id}')
def add_product(vendor_id: str, request: schema.Product, service=Depends(get_product_service)):
    product = service.add_product(request, vendor_id)
    return product


@router.get('/get_product/{vendor_id}')
def get_product(vendor_id: str, service=Depends(get_product_service)):
    try:
        products = service.get_products(vendor_id)
        return products

    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/get_all_product')
def get_all_product(service=Depends(get_product_service)):
    try:
        products = service.get_all_products()
        return products
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


# needs rewrite
# @router.get('/get_nearby_products/{address_id}')
# def get_nearby_products(address_id: str, db: Session = Depends(get_db)):
#     customer_address = db.query(model.CustomerAddress).filter(model.CustomerAddress.address_id == address_id).first()
#     if not customer_address:
#         raise HTTPException(status_code=404, detail="No such Address")
#     customer_latitude = customer_address.latitude
#     customer_longitude = customer_address.longitude
#     vendors = db.query(model.VendorAddress).all()
#     nearby_vendors = []
#     for vendor in vendors:
#         if vendor.latitude is None or vendor.longitude is None:
#             continue
#         distance = haversine(customer_latitude, customer_longitude, vendor.latitude, vendor.longitude)
#         if distance < 5:
#             nearby_vendors.append(vendor.vendor_id)
#     if not nearby_vendors:
#         raise HTTPException(status_code=404, detail="No nearby vendors found")
#     nearby_products = db.query(model.Product).filter(model.Product.vendor_id.in_(nearby_vendors)).all()
#     return nearby_products


@router.put('/update_product/{product_id}')
def update_product(product_id: str, request: schema.Product, service=Depends(get_product_service)):
    try:
        updated_product = service.update_product(product_id, request)
        return updated_product
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/delete_product/{product_id}')
def delete_product(product_id: str, service=Depends(get_product_service)):
    try:
        service.delete_product(product_id)
        return "Deleted Successfully"
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
