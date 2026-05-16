from fastapi import Depends, HTTPException, APIRouter

from controller import schema
from controller.dependency.vendor_dependency import get_vendor_service
from domain.exception import InvalidOTP, VendorNotFound
from service.auth_service import create_access_token
from controller.dependency.auth_dependency import get_current_user

router = APIRouter()


@router.post('/request_otp')
def request_otp(contact: str, service=Depends(get_vendor_service)):
    otp = service.request_otp(contact)
    return "OTP Sent Successfully " + otp  # remove it after testing


@router.post('/verify_otp')
def verify_otp(contact: str, vendor_otp: str, service=Depends(get_vendor_service)):
    try:
        vendor_id = service.verify_otp(contact, vendor_otp)
        token = create_access_token(
            {"user_id": vendor_id,
             "role": "vendor"
             })
        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except InvalidOTP as e:
        raise HTTPException(detail=str(e), status_code=404)


@router.get('/get_vendor')
def get_vendor(user=Depends(get_current_user), service=Depends(get_vendor_service)):
    try:
        if user["role"] != "vendor":
            raise HTTPException(403)
        vendor_id = user['user_id']
        vendor = service.get_vendor_by_id(vendor_id)
        return vendor

    except VendorNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/all_vendors')
def get_all_vendors(service=Depends(get_vendor_service)):
    vendors = service.get_all_vendors()
    return vendors


@router.put('/update_vendor')
def update_vendor(request: schema.Vendor, service=Depends(get_vendor_service), user=Depends(get_current_user)):
    try:
        if user["role"] != "vendor":
            raise HTTPException(403)
        vendor_id = user['user_id']
        updated_vendor = service.update_vendor(vendor_id, request)
        return updated_vendor

    except VendorNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/delete_vendor')
def delete_vendor(user=Depends(get_current_user), service=Depends(get_vendor_service)):
    try:
        if user["role"] != "vendor":
            raise HTTPException(403)
        vendor_id = user['user_id']
        service.delete_vendor(vendor_id)
        return 'successfully deleted'

    except VendorNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
