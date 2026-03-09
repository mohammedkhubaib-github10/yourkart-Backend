from abc import ABC, abstractmethod


class CartRepo(ABC):
    @abstractmethod
    def create_cart(self, customer_id):
        pass

    @abstractmethod
    def get_cart_by_id(self, customer_id):
        pass

    @abstractmethod
    def add_items_to_cart(self, cart_id, product_id):
        pass

    @abstractmethod
    def view_cart_items(self, cart_id):
        pass

    @abstractmethod
    def delete_cart_items(self, item_id):
        pass
