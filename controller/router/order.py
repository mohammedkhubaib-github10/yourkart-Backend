from fastapi import Depends, HTTPException, APIRouter

from controller import schema
from controller.dependency.order_dependency import get_order_service
from domain.exception import PaymentFailure, CartItemsNotFound, OrderNotFound

router = APIRouter()


@router.post('/place_order/{customer_id}')
def place_order(customer_id: str, request: schema.Order, service=Depends(get_order_service)):
    try:
        order = service.place_order(customer_id, request)
        return order
    except PaymentFailure as e:
        raise HTTPException(status_code=500, detail=str(e))
    except CartItemsNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/get_customer_orders/{customer_id}')
def view_customer_orders(customer_id: str, service=Depends(get_order_service)):
    try:
        orders = service.view_customer_orders(customer_id)
        return orders
    except OrderNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/get_vendor_orders/{vendor_id}')
def get_vendor_orders(vendor_id: str, service=Depends(get_order_service)):
    try:
        orders = service.view_vendor_orders(vendor_id)
        return orders
    except OrderNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

