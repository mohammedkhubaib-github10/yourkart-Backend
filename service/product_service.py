from domain.exception import ProductNotFound
from domain.repository import ProductRepo


class ProductService:
    def __init__(self, repo: ProductRepo):
        self.repo = repo

    def add_product(self, request, vendor_id):
        product = self.repo.add_product(request, vendor_id)
        return product

    def get_products(self, vendor_id):
        products = self.repo.get_products(vendor_id)
        if not products:
            raise ProductNotFound()
        return products

    def get_product_by_id(self, vendor_id, product_id):
        product = self.repo.get_product_by_id(vendor_id, product_id)
        if not product:
            raise ProductNotFound()
        return product

    def get_all_products(self):
        products = self.repo.get_all_products()
        if not products:
            raise ProductNotFound()
        return products

    def update_product(self, vendor_id, product_id, request):
        try:
            self.get_product_by_id(vendor_id, product_id)
            updated_product = self.repo.update_product(vendor_id, product_id, request)
            return updated_product

        except ProductNotFound:
            raise ProductNotFound()

    def delete_product(self, vendor_id, product_id):
        try:
            self.get_product_by_id(vendor_id, product_id)
            self.repo.delete_product(vendor_id, product_id)

        except ProductNotFound:
            raise ProductNotFound()
