from datetime import datetime

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from infrastructure import model
from controller import schema
from infrastructure.database.session import get_db

router = APIRouter()


@router.post('/place_order/{cart_id}')
def place_order(cart_id: str, request: schema.Order, db: Session = Depends(get_db)):
    try:
        cart = db.query(model.Cart).filter(model.Cart.cart_id == cart_id).first()
        items_query = db.query(model.CartItem).filter(model.CartItem.cart_id == cart_id)
        items = items_query.all()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart Not Found")
        if cart.amount == 0:
            raise HTTPException(status_code=404, detail="Empty Cart")

        payment_status_str = "failed"
        is_cod = request.payment_mode == schema.PaymentMode.COD
        order = model.Order(total_price=cart.amount, customer_id=cart.customer_id, cart_id=cart.cart_id,
                            payment_mode=request.payment_mode,
                            order_status=schema.OrderStatus.Placed if is_cod or payment_status_str == "success" else schema.OrderStatus.Failed,
                            delivery_address_id=request.delivery_address_id,
                            created_at=request.created_at)
        db.add(order)
        db.flush()
        if not is_cod:
            payment = model.Payment(payment_mode=request.payment_mode, payment_amount=cart.amount,
                                    payment_status=schema.PaymentStatus.Success if payment_status_str == "success" else schema.PaymentStatus.Failed,
                                    order_id=order.order_id, payment_on=datetime.now())
            db.add(payment)
        if order.order_status == schema.OrderStatus.Placed:
            for item in items:
                order_item = model.OrderItem(
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
    order = db.query(model.Order).filter(model.Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order does not exist")
    db.delete(order)
    db.commit()
    return 'Successful'


@router.get('/get_customer_orders/{customer_id}')
def get_customer_orders(customer_id: str, db: Session = Depends(get_db)):
    orders = db.query(model.Order).filter(model.Order.customer_id == customer_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No Orders Found")

    result = []
    for order in orders:
        items = db.query(model.OrderItem).filter(model.OrderItem.order_id == order.order_id).all()
        result.append({
            "order_id": order.order_id,
            "total_price": order.total_price,
            "status": order.order_status,
            "payment": order.payment_mode,
            "created_at": order.created_at,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": db.query(model.Product).filter(
                        model.Product.product_id == item.product_id).first().product_name,
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
            model.Order.order_id,
            model.Order.total_price,
            model.Order.created_at,
            model.Customer.customer_name,
            model.Customer.contact,
            model.CustomerAddress.street,
            model.CustomerAddress.city,
            model.CustomerAddress.pincode,
            model.CustomerAddress.flat_no,
            model.Product.product_name,
            model.OrderItem.qty,
            model.OrderItem.total_price,
            model.Order.payment_mode
        )
        .join(model.OrderItem, model.Order.order_id == model.OrderItem.order_id)
        .join(model.Product, model.OrderItem.product_id == model.Product.product_id)
        .join(model.Customer, model.Order.customer_id == model.Customer.customer_id)
        .join(model.CustomerAddress, model.Order.delivery_address_id == model.CustomerAddress.address_id)
        .filter(model.Product.vendor_id == vendor_id, model.Order.order_status == schema.OrderStatus.Placed)
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
