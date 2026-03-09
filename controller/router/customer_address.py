from fastapi import Depends, HTTPException, APIRouter

from controller import schema
from controller.dependency.customer_address_dependency import get_customer_address_service
from domain.exception import CustomerAddressNotFound

router = APIRouter()


@router.post('/new_customer_address/{customer_id}')
def add_address(customer_id: str, request: schema.CustomerAddress, service=Depends(get_customer_address_service)):
    address = service.add_address(customer_id, request)
    return address


@router.get('/get_customer_addresses/{customer_id}')
def get_addresses(customer_id: str, service=Depends(get_customer_address_service)):
    try:
        addresses = service.get_addresses(customer_id)
        return addresses
    except CustomerAddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put('/update_customer_address/{address_id}')
def update_address(address_id: str, request: schema.CustomerAddress, service=Depends(get_customer_address_service)):
    try:
        updated_address = service.update_address(address_id, request)
        return updated_address
    except CustomerAddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/delete_customer_address/{address_id}')
def delete_address(address_id: str, service=Depends(get_customer_address_service)):
    try:
        service.delete_address(address_id)
        return "Successfully Deleted"
    except CustomerAddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
