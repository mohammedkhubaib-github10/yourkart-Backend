from domain.exception import CartNotFound, CartItemsNotFound, PaymentFailure
from domain.repository import OrderRepo, CartRepo
from infrastructure.enums.enums import PaymentMode
from service.payment_service import PaymentService


class OrderService:
    def __init__(self, repo: OrderRepo, cart_repo: CartRepo, payment_service: PaymentService):
        self.repo = repo
        self.cart_repo = cart_repo
        self.payment_service = payment_service

    def place_order(self, customer_id, request):
        cart = self.cart_repo.get_cart_by_id(customer_id)
        if not cart:
            raise CartNotFound()
        if cart.amount == 0:
            raise CartItemsNotFound()
        order = self.repo.place_order(cart, request)
        is_cod = request.payment_mode == PaymentMode.COD
        if is_cod:
            return self.confirm_order(cart, order)
        try:
            self.payment_service.make_payment(order)
            return self.confirm_order(cart, order)
        except PaymentFailure:
            raise PaymentFailure()

    def view_customer_orders(self, customer_id):
        pass

    def view_vendor_orders(self, vendor_id):
        pass

    def confirm_order(self, cart, order):
        return self.repo.confirm_order(cart, order)
