from fastapi import Depends, HTTPException, APIRouter

from controller import schema
from controller.dependency.vendor_address_dependency import get_vendor_address_service
from domain.exception import VendorAddressNotFound

router = APIRouter()


@router.post('/new_vendor_address/{vendor_id}')
def add_address(vendor_id: str, request: schema.VendorAddress, service=Depends(get_vendor_address_service)):
    address = service.add_address(vendor_id, request)
    return address


@router.get('/get_vendor_addresses/{vendor_id}')
def get_addresses(vendor_id: str, service=Depends(get_vendor_address_service)):
    try:
        addresses = service.get_addresses(vendor_id)
        return addresses
    except VendorAddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put('/update_vendor_address/{address_id}')
def update_address(address_id: str, request: schema.VendorAddress, service=Depends(get_vendor_address_service)):
    try:
        updated_address = service.update_address(address_id, request)
        return updated_address
    except VendorAddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/delete_vendor_address/{address_id}')
def delete_address(address_id: str, service=Depends(get_vendor_address_service)):
    try:
        service.delete_address(address_id)
        return 'Successfully Deleted'
    except VendorAddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
