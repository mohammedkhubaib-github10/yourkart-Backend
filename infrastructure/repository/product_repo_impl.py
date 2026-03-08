from datetime import datetime

from domain.repository import ProductRepo
from infrastructure import model


class ProductRepoImpl(ProductRepo):
    def __init__(self, db):
        self.db = db

    def add_product(self, request, vendor_id):
        product = model.Product(product_name=request.product_name, product_image=request.product_image,
                                price=request.price, vendor_id=vendor_id, created_at=datetime.utcnow())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_products(self, vendor_id):
        products = self.db.query(model.Product).filter(model.Product.vendor_id == vendor_id).all()
        return products

    def get_all_products(self):
        products = self.db.query(model.Product).all()
        return products

    def get_product_by_id(self, product_id):
        product = self.db.query(model.Product).filter(model.Product.product_id == product_id).first()
        return product

    def update_product(self, product_id, request):
        product_query = self.db.query(model.Product).filter(model.Product.product_id == product_id)
        product = product_query.first()
        product_query.update(request.model_dump())
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id):
        product_query = self.db.query(model.Product).filter(model.Product.product_id == product_id)
        product = product_query.first()
        self.db.delete(product)
        self.db.commit()
