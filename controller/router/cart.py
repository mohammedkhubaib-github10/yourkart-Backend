from fastapi import Depends, HTTPException, APIRouter

from controller.dependency.cart_dependency import get_cart_service
from domain.exception import CartItemsNotFound

router = APIRouter()


# Query Optimization
@router.get('/view_cart_items/{customer_id}')
def view_cart_items(customer_id: str, service=Depends(get_cart_service)):
    try:
        items = service.view_cart_items(customer_id)
        return items
    except CartItemsNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post('/add_items/{customer_id}/{product_id}')
def add_items_to_cart(customer_id: str, product_id: str, service=Depends(get_cart_service)):
    item = service.add_items_to_cart(product_id, customer_id)
    return item


@router.delete('/delete_items/{item_id}')
def delete_cart_item(item_id: str, service=Depends(get_cart_service)):
    service.delete_cart_items(item_id)
    return "successfully Deleted"
