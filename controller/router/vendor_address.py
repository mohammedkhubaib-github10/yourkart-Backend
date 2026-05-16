from fastapi import Depends, HTTPException, APIRouter

from controller import schema
from controller.dependency.vendor_address_dependency import get_vendor_address_service
from domain.exception import VendorAddressNotFound
from controller.dependency.auth_dependency import get_current_user

router = APIRouter()


@router.post('/new_vendor_address')
def add_address(request: schema.VendorAddress, service=Depends(get_vendor_address_service),
                user=Depends(get_current_user)):
    if user["role"] != "vendor":
        raise HTTPException(403)
    vendor_id = user['user_id']
    address = service.add_address(vendor_id, request)
    return address


@router.get('/get_vendor_addresses')
def get_addresses(user=Depends(get_current_user), service=Depends(get_vendor_address_service)):
    try:
        if user["role"] != "vendor":
            raise HTTPException(403)
        vendor_id = user['user_id']
        addresses = service.get_addresses(vendor_id)
        return addresses
    except VendorAddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put('/update_vendor_address/{address_id}')
def update_address(address_id: str, request: schema.VendorAddress, service=Depends(get_vendor_address_service),
                   user=Depends(get_current_user)):
    try:
        if user["role"] != "vendor":
            raise HTTPException(403)
        vendor_id = user['user_id']
        updated_address = service.update_address(vendor_id, address_id, request)
        return updated_address
    except VendorAddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/delete_vendor_address/{address_id}')
def delete_address(address_id: str, service=Depends(get_vendor_address_service), user=Depends(get_current_user)):
    try:
        if user["role"] != "vendor":
            raise HTTPException(403)
        vendor_id = user['user_id']
        service.delete_address(vendor_id, address_id)
        return 'Successfully Deleted'
    except VendorAddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
