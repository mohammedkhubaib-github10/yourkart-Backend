from abc import ABC, abstractmethod


class OrderRepo(ABC):
    @abstractmethod
    def place_order(self, cart, request):
        pass

    @abstractmethod
    def view_customer_orders(self, customer_id):
        pass

    @abstractmethod
    def view_vendor_orders(self, vendor_id):
        pass

    @abstractmethod
    def confirm_order(self, cart, order):
        pass
