from datetime import datetime

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import models
import schemas
from core.database import get_db

router = APIRouter()


@router.post('/place_order/{cart_id}')
def place_order(cart_id: str, request: schemas.Order, db: Session = Depends(get_db)):
    try:
        cart = db.query(models.Cart).filter(models.Cart.cart_id == cart_id).first()
        items_query = db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id)
        items = items_query.all()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart Not Found")
        if cart.amount == 0:
            raise HTTPException(status_code=404, detail="Empty Cart")

        payment_status_str = "failed"
        is_cod = request.payment_mode == schemas.PaymentMode.COD
        order = models.Order(total_price=cart.amount, customer_id=cart.customer_id, cart_id=cart.cart_id,
                             payment_mode=request.payment_mode,
                             order_status=schemas.OrderStatus.Placed if is_cod or payment_status_str == "success" else schemas.OrderStatus.Failed,
                             delivery_address_id=request.delivery_address_id,
                             created_at=request.created_at)
        db.add(order)
        db.flush()
        if not is_cod:
            payment = models.Payment(payment_mode=request.payment_mode, payment_amount=cart.amount,
                                     payment_status=schemas.PaymentStatus.Success if payment_status_str == "success" else schemas.PaymentStatus.Failed,
                                     order_id=order.order_id, payment_on=datetime.now())
            db.add(payment)
        if order.order_status == schemas.OrderStatus.Placed:
            for item in items:
                order_item = models.OrderItem(
                    order_id=order.order_id,
                    product_id=item.product_id,
                    qty=item.qty,
                    total_price=item.total_price
                )
                db.add(order_item)
            items_query.delete(synchronize_session=False)
            cart.amount = 0
        db.commit()
        db.refresh(order)
        return order
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Order placement failed")


@router.delete('/delete_order/{order_id}')
def delete_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order does not exist")
    db.delete(order)
    db.commit()
    return 'Successful'


@router.get('/get_customer_orders/{customer_id}')
def get_customer_orders(customer_id: str, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No Orders Found")

    result = []
    for order in orders:
        items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order.order_id).all()
        result.append({
            "order_id": order.order_id,
            "total_price": order.total_price,
            "status": order.order_status,
            "payment": order.payment_mode,
            "created_at": order.created_at,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": db.query(models.Product).filter(
                        models.Product.product_id == item.product_id).first().product_name,
                    "qty": item.qty,
                    "total_price": item.total_price
                } for item in items
            ]
        })

    return result


@router.get('/get_vendor_orders/{vendor_id}')
def get_vendor_orders(vendor_id: str, db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Order.order_id,
            models.Order.total_price,
            models.Order.created_at,
            models.Customer.customer_name,
            models.Customer.contact,
            models.CustomerAddress.street,
            models.CustomerAddress.city,
            models.CustomerAddress.pincode,
            models.CustomerAddress.flat_no,
            models.Product.product_name,
            models.OrderItem.qty,
            models.OrderItem.total_price,
            models.Order.payment_mode
        )
        .join(models.OrderItem, models.Order.order_id == models.OrderItem.order_id)
        .join(models.Product, models.OrderItem.product_id == models.Product.product_id)
        .join(models.Customer, models.Order.customer_id == models.Customer.customer_id)
        .join(models.CustomerAddress, models.Order.delivery_address_id == models.CustomerAddress.address_id)
        .filter(models.Product.vendor_id == vendor_id, models.Order.order_status == schemas.OrderStatus.Placed)
        .all()
    )
    response = []
    for row in results:
        response.append({
            "order_id": row[0],
            "total_price": row[1],
            "created_at": row[2],
            "customer_name": row[3],
            "customer_contact": row[4],
            "customer_street": row[5],
            "customer_city": row[6],
            "customer_pincode": row[7],
            "customer_flat_no": row[8],
            "product_name": row[9],
            "qty": row[10],
            "item_total_price": row[11],
            "payment_mode": row[12]
        })
        if not response:
            raise HTTPException(status_code=400, detail="No Orders Found")
    return response
