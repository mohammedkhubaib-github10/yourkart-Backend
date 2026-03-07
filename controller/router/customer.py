from fastapi import HTTPException, Depends, APIRouter

from controller import schema
from controller.dependency.customer_dependency import get_customer_service
from domain.exception.auth_exception import InvalidOTP
from domain.exception.customer_exception import CustomerNotFound

router = APIRouter()


@router.post('/request_otp')
def request_otp(contact: str, service=Depends(get_customer_service)):
    otp = service.request_otp(contact)
    return "OTP Sent Successfully " + otp  # remove it after testing


@router.post('/verify_otp')
def verify_otp(contact: str, customer_otp: str, service=Depends(get_customer_service)):
    try:
        customer = service.verify_otp(contact, customer_otp)
        return f'logged in Successfully, {customer.customer_id}'

    except InvalidOTP as e:
        raise HTTPException(detail=str(e), status_code=404)


@router.get('/get_customer/{customer_id}')
def get_customer(customer_id: str, service=Depends(get_customer_service)):
    try:
        customer = service.get_customer_by_id(customer_id)
        return customer

    except CustomerNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/all_customers')
def get_all_customers(service=Depends(get_customer_service)):
    customers = service.get_all_customers()
    return customers


@router.put('/update_customer/{customer_id}')
def update_customer(customer_id: str, request: schema.Customer, service=Depends(get_customer_service)):
    try:
        updated_customer = service.update_customer(customer_id, request.model_dump())
        return updated_customer

    except CustomerNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/delete_customer/{customer_id}')
def delete_customer(customer_id: str, service=Depends(get_customer_service)):
    try:
        service.delete_customer(customer_id)
        return 'successfully deleted'

    except CustomerNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
