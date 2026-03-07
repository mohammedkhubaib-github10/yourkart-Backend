from fastapi import Depends, HTTPException, APIRouter

from controller import schema
from controller.dependency.vendor_dependency import get_vendor_service
from domain.exception import InvalidOTP, VendorNotFound

router = APIRouter()


@router.post('/request_otp')
def request_otp(contact: str, service=Depends(get_vendor_service)):
    otp = service.request_otp(contact)
    return "OTP Sent Successfully " + otp  # remove it after testing


@router.post('/verify_otp')
def verify_otp(contact: str, vendor_otp: str, service=Depends(get_vendor_service)):
    try:
        vendor = service.verify_otp(contact, vendor_otp)
        return f'logged in Successfully, {vendor.vendor_id}'

    except InvalidOTP as e:
        raise HTTPException(detail=str(e), status_code=404)


@router.get('/get_vendor/{vendor_id}')
def get_vendor(vendor_id: str, service=Depends(get_vendor_service)):
    try:
        vendor = service.get_vendor_by_id(vendor_id)
        return vendor

    except VendorNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/all_vendors')
def get_all_vendors(service=Depends(get_vendor_service)):
    vendors = service.get_all_vendors()
    return vendors


@router.put('/update_vendor/{vendor_id}')
def update_vendor(vendor_id: str, request: schema.Vendor, service=Depends(get_vendor_service)):
    try:
        updated_vendor = service.update_vendor(vendor_id, request.model_dump())
        return updated_vendor

    except VendorNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/delete_vendor/{vendor_id}')
def delete_vendor(vendor_id: str, service=Depends(get_vendor_service)):
    try:
        service.delete_vendor(vendor_id)
        return 'successfully deleted'

    except VendorNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
