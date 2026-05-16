from fastapi import Depends, HTTPException, APIRouter

from controller import schema
from controller.dependency.order_dependency import get_order_service
from domain.exception import PaymentFailure, CartItemsNotFound, OrderNotFound
from controller.dependency.auth_dependency import get_current_user

router = APIRouter()


@router.post('/place_order')
def place_order(request: schema.Order, service=Depends(get_order_service),
                user=Depends(get_current_user)):
    try:
        if user["role"] != "customer":
            raise HTTPException(403)
        customer_id = user['user_id']
        order = service.place_order(customer_id, request)
        return order
    except PaymentFailure as e:
        raise HTTPException(status_code=500, detail=str(e))
    except CartItemsNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/get_customer_orders')
def view_customer_orders(service=Depends(get_order_service), user=Depends(get_current_user)):
    try:
        if user["role"] != "customer":
            raise HTTPException(403)
        customer_id = user['user_id']
        orders = service.view_customer_orders(customer_id)
        return orders
    except OrderNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/get_vendor_orders')
def get_vendor_orders(service=Depends(get_order_service), user=Depends(get_current_user)):
    try:
        if user["role"] != "vendor":
            raise HTTPException(403)
        vendor_id = user['user_id']
        orders = service.view_vendor_orders(vendor_id)
        return orders
    except OrderNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
