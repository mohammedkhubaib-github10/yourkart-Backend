from fastapi import Depends, HTTPException, APIRouter

from controller.dependency.auth_dependency import get_current_user
from controller.dependency.cart_dependency import get_cart_service
from domain.exception import CartItemsNotFound, ProductNotFound, CartItemsOfDifferentVendor, CartNotFound

router = APIRouter()


# Query Optimization
@router.get('/view_cart_items')
def view_cart_items(service=Depends(get_cart_service), user=Depends(get_current_user)):
    try:
        if user["role"] != "customer":
            raise HTTPException(403)
        customer_id = user['user_id']
        items = service.view_cart_items(customer_id)
        return items
    except CartItemsNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post('/add_items/{product_id}')
def add_items_to_cart(product_id: str, service=Depends(get_cart_service), user=Depends(get_current_user)):
    if user["role"] != "customer":
        raise HTTPException(403)
    customer_id = user['user_id']
    try:
        item = service.add_items_to_cart(product_id, customer_id)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CartItemsOfDifferentVendor as e:
        raise HTTPException(status_code=400, detail=str(e))
    return item


@router.delete('/delete_items/{item_id}')
def delete_cart_item(item_id: str, service=Depends(get_cart_service), user=Depends(get_current_user)):
    if user["role"] != "customer":
        raise HTTPException(403)
    customer_id = user['user_id']
    try:
        service.delete_cart_items(customer_id, item_id)
    except CartItemsNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CartNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    return "successfully Deleted"
