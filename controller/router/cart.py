from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from infrastructure import model
from infrastructure.database.session import get_db
from service.helper import update_cart_amount

router = APIRouter()


@router.post('/add_cart/{customer_id}')
def add_cart(customer_id: str, db: Session = Depends(get_db)):
    existing_cart = db.query(model.Cart).filter(model.Cart.customer_id == customer_id).first()
    if existing_cart:
        raise HTTPException(status_code=400, detail="Already Cart Exists")
    cart = model.Cart(customer_id=customer_id)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


# Query Optimization
@router.get('/view_cart_items/{cart_id}')
def view_items(cart_id: str, db: Session = Depends(get_db)):
    cart = db.query(model.Cart).filter(model.Cart.cart_id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart does not exists")
    cart_items = db.query(model.CartItem).filter(model.CartItem.cart_id == cart_id).all()
    items = []
    for item in cart_items:
        product = db.query(model.Product).filter(model.Product.product_id == item.product_id).first()
        items.append({
            "item_id": item.item_id,
            "product_id": item.product_id,
            "product_name": product.product_name if product else "Unknown",
            "product_image": product.product_image if product else None,
            "qty": item.qty,
            "price_per_unit": product.price if product else None,
            "total_price": item.total_price
        })

    return {
        "cart_id": cart.cart_id,
        "customer_id": cart.customer_id,
        "total_amount": cart.amount,
        "items": items
    }


@router.post('/add_items/{cart_id}/{product_id}')
def add_items(cart_id: str, product_id: str, db: Session = Depends(get_db)):
    cart = db.query(model.Cart).filter(model.Cart.cart_id == cart_id).first()
    existing_items = db.query(model.CartItem, model.Product).join(model.Product,
                                                                  model.CartItem.product_id == model.Product.product_id).filter(
        model.CartItem.cart_id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart doesn't Exist")

    item_query = db.query(model.CartItem).filter(model.CartItem.cart_id == cart_id,
                                                 model.CartItem.product_id == product_id)
    item = item_query.first()
    product_query = db.query(model.Product).filter(model.Product.product_id == product_id)
    product = product_query.first()
    if existing_items:
        if existing_items.Product.vendor_id != product.vendor_id:
            raise HTTPException(status_code=400, detail="Cannot add products of a different vendor")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if item:
        item.qty += 1
        item.total_price = product.price * item.qty
    else:
        item = model.CartItem(
            cart_id=cart_id, product_id=product_id, total_price=product.price
        )
        db.add(item)

    db.commit()
    db.refresh(item)

    update_cart_amount(cart_id, product.price, db, True)
    return item


@router.delete('/delete_items/{cart_id}/{item_id}')
def delete_item(item_id: str, cart_id: str, db: Session = Depends(get_db)):
    item_query = db.query(model.CartItem).filter(model.CartItem.item_id == item_id,
                                                 model.CartItem.cart_id == cart_id)
    item = item_query.first()
    if not item:
        raise HTTPException(status_code=404, detail="Item does not exist")
    item_price = item.total_price / item.qty
    if item.qty == 1:
        db.delete(item)
    else:
        item.qty -= 1
        item.total_price = item.qty * item_price
    db.commit()

    update_cart_amount(cart_id, item_price, db, False)
    return "successful"
