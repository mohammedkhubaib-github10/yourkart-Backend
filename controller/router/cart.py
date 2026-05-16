from fastapi import Depends, HTTPException, APIRouter

from controller.dependency.auth_dependency import get_current_user
from controller.dependency.cart_dependency import get_cart_service
from domain.exception import CartItemsNotFound

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
    item = service.add_items_to_cart(product_id, customer_id)
    return item


@router.delete('/delete_items/{item_id}')
def delete_cart_item(item_id: str, service=Depends(get_cart_service), user=Depends(get_current_user)):
    if user["role"] != "customer":
        raise HTTPException(403)
    customer_id = user['user_id']
    service.delete_cart_items(customer_id, item_id)
    return "successfully Deleted"
