from datetime import datetime

from domain.repository import OrderRepo
from infrastructure import model
from infrastructure.enums import OrderStatus


class OrderRepoImpl(OrderRepo):

    def __init__(self, db):
        self.db = db

    def place_order(self, cart, request):
        order = model.Order(total_price=cart.amount, customer_id=cart.customer_id, cart_id=cart.cart_id,
                            payment_mode=request.payment_mode,
                            order_status=OrderStatus.Pending,
                            delivery_address_id=request.delivery_address_id,
                            created_at=datetime.utcnow())
        self.db.add(order)
        return order

    def view_customer_orders(self, customer_id):
        orders = self.db.query(model.Order).filter(model.Order.customer_id == customer_id).all()
        if not orders:
            return
        result = []
        for order in orders:
            items = self.db.query(model.Product, model.OrderItem) \
                .join(model.Product, model.OrderItem.product_id == model.Product.product_id) \
                .filter(model.OrderItem.order_id == order.order_id) \
                .all()
            result.append({
                "order_id": order.order_id,
                "total_price": order.total_price,
                "status": order.order_status,
                "payment": order.payment_mode,
                "created_at": order.created_at,
                "items": [
                    {
                        "product_id": product.product_id,
                        "product_name": product.product_name,
                        "qty": order_item.qty,
                        "total_price": order_item.total_price
                    } for product, order_item in items
                ]
            })

        return result

    def view_vendor_orders(self, vendor_id):
        pass

    def confirm_order(self, cart, order):
        self.db.commit()
        order.order_status = OrderStatus.Placed
        items_query = self.db.query(model.CartItem).filter(model.CartItem.cart_id == order.cart_id)
        items = items_query.all()
        for item in items:
            order_item = model.OrderItem(
                order_id=order.order_id,
                product_id=item.product_id,
                qty=item.qty,
                total_price=item.total_price
            )
            self.db.add(order_item)
        items_query.delete(synchronize_session=False)
        cart.amount = 0
        self.db.commit()
        self.db.refresh(order)
        return order
