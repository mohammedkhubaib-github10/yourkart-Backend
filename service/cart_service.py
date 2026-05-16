from domain.exception import CartNotFound, ProductNotFound, CartItemsOfDifferentVendor, CartItemsNotFound
from domain.repository import CartRepo


class CartService:
    def __init__(self, repo: CartRepo):
        self.repo = repo

    def create_cart(self, customer_id):
        cart = self.repo.create_cart(customer_id)
        return cart

    def get_cart_by_id(self, customer_id):
        cart = self.repo.get_cart_by_id(customer_id)
        if not cart:
            raise CartNotFound()
        return cart

    def add_items_to_cart(self, product_id, customer_id):
        try:
            cart = self.get_cart_by_id(customer_id)
        except CartNotFound:
            cart = self.create_cart(customer_id)
        except ProductNotFound:
            raise ProductNotFound
        except CartItemsOfDifferentVendor:
            raise CartItemsOfDifferentVendor
        item = self.repo.add_items_to_cart(cart.cart_id, product_id)
        return item

    def view_cart_items(self, customer_id):
        try:
            cart = self.get_cart_by_id(customer_id)

        except CartNotFound:
            cart = self.create_cart(customer_id)

        cart_items = self.repo.view_cart_items(cart.cart_id)
        return cart_items

    def delete_cart_items(self, customer_id, item_id):
        try:
            self.repo.delete_cart_items(customer_id, item_id)
        except CartItemsNotFound:
            raise CartItemsNotFound
        except CartNotFound:
            raise  CartNotFound
