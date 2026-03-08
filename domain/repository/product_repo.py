from abc import ABC, abstractmethod


class ProductRepo(ABC):
    @abstractmethod
    def add_product(self, request, vendor_id):
        pass

    @abstractmethod
    def get_products(self, vendor_id):
        pass

    @abstractmethod
    def get_all_products(self):
        pass

    @abstractmethod
    def get_product_by_id(self, product_id):
        pass

    @abstractmethod
    def update_product(self, product_id, request):
        pass

    @abstractmethod
    def delete_product(self, product_id):
        pass
