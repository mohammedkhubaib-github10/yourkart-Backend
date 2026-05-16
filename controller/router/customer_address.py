from fastapi import Depends, HTTPException, APIRouter

from controller import schema
from controller.dependency.customer_address_dependency import get_customer_address_service
from domain.exception import CustomerAddressNotFound
from controller.dependency.auth_dependency import get_current_user

router = APIRouter()


@router.post('/new_customer_address')
def add_address(request: schema.CustomerAddress, service=Depends(get_customer_address_service),
                user=Depends(get_current_user)):
    if user["role"] != "customer":
        raise HTTPException(403)
    customer_id = user['user_id']
    address = service.add_address(customer_id, request)
    return address


@router.get('/get_customer_addresses')
def get_addresses(service=Depends(get_customer_address_service), user=Depends(get_current_user)):
    try:
        if user["role"] != "customer":
            raise HTTPException(403)
        customer_id = user['user_id']
        addresses = service.get_addresses(customer_id)
        return addresses
    except CustomerAddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put('/update_customer_address/{address_id}')
def update_address(address_id: str, request: schema.CustomerAddress, service=Depends(get_customer_address_service),
                   user=Depends(get_current_user)):
    try:
        if user["role"] != "customer":
            raise HTTPException(403)
        customer_id = user['user_id']
        updated_address = service.update_address(customer_id, address_id, request)
        return updated_address
    except CustomerAddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/delete_customer_address/{address_id}')
def delete_address(address_id: str, service=Depends(get_customer_address_service), user=Depends(get_current_user)):
    try:
        if user["role"] != "customer":
            raise HTTPException(403)
        customer_id = user['user_id']
        service.delete_address(customer_id, address_id)
        return "Successfully Deleted"
    except CustomerAddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
