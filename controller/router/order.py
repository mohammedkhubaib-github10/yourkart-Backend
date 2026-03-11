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


# @router.get('/get_vendor_orders/{vendor_id}')
# def get_vendor_orders(vendor_id: str, db: Session = Depends(get_db)):
#     results = (
#         db.query(
#             model.Order.order_id,
#             model.Order.total_price,
#             model.Order.created_at,
#             model.Customer.customer_name,
#             model.Customer.contact,
#             model.CustomerAddress.street,
#             model.CustomerAddress.city,
#             model.CustomerAddress.pincode,
#             model.CustomerAddress.flat_no,
#             model.Product.product_name,
#             model.OrderItem.qty,
#             model.OrderItem.total_price,
#             model.Order.payment_mode
#         )
#         .join(model.OrderItem, model.Order.order_id == model.OrderItem.order_id)
#         .join(model.Product, model.OrderItem.product_id == model.Product.product_id)
#         .join(model.Customer, model.Order.customer_id == model.Customer.customer_id)
#         .join(model.CustomerAddress, model.Order.delivery_address_id == model.CustomerAddress.address_id)
#         .filter(model.Product.vendor_id == vendor_id, model.Order.order_status == schema.OrderStatus.Placed)
#         .all()
#     )
#     response = []
#     for row in results:
#         response.append({
#             "order_id": row[0],
#             "total_price": row[1],
#             "created_at": row[2],
#             "customer_name": row[3],
#             "customer_contact": row[4],
#             "customer_street": row[5],
#             "customer_city": row[6],
#             "customer_pincode": row[7],
#             "customer_flat_no": row[8],
#             "product_name": row[9],
#             "qty": row[10],
#             "item_total_price": row[11],
#             "payment_mode": row[12]
#         })
#         if not response:
#             raise HTTPException(status_code=400, detail="No Orders Found")
#     return response
