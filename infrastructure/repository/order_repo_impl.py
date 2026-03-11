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
        pass

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
