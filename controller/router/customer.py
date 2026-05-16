from fastapi import HTTPException, Depends, APIRouter

from controller import schema
from controller.dependency.auth_dependency import get_current_user
from controller.dependency.customer_dependency import get_customer_service
from domain.exception.auth_exception import InvalidOTP
from domain.exception.customer_exception import CustomerNotFound
from service.auth_service import create_access_token

router = APIRouter()


@router.post('/request_otp')
def request_otp(contact: str, service=Depends(get_customer_service)):
    otp = service.request_otp(contact)
    return "OTP Sent Successfully " + otp  # remove it after testing


@router.post('/verify_otp')
def verify_otp(contact: str, customer_otp: str, service=Depends(get_customer_service)):
    try:
        customer_id = service.verify_otp(contact, customer_otp)
        token = create_access_token({"user_id": customer_id, "role": "customer"})
        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except InvalidOTP as e:
        raise HTTPException(detail=str(e), status_code=404)


@router.get('/get_customer')
def get_customer(user=Depends(get_current_user), service=Depends(get_customer_service)):
    try:
        if user["role"] != "customer":
            raise HTTPException(403)
        customer_id = user['user_id']
        customer = service.get_customer_by_id(customer_id)
        return customer

    except CustomerNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/all_customers')
def get_all_customers(service=Depends(get_customer_service)):
    customers = service.get_all_customers()
    return customers


@router.put('/update_customer')
def update_customer(request: schema.Customer, service=Depends(get_customer_service), user=Depends(get_current_user)):
    try:
        if user["role"] != "customer":
            raise HTTPException(403)
        customer_id = user['user_id']
        updated_customer = service.update_customer(customer_id, request)
        return updated_customer

    except CustomerNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/delete_customer')
def delete_customer(service=Depends(get_customer_service), user=Depends(get_current_user)):
    try:
        if user["role"] != "customer":
            raise HTTPException(403)
        customer_id = user['user_id']
        service.delete_customer(customer_id)
        return 'successfully deleted'

    except CustomerNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
