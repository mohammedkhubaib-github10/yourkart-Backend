from datetime import datetime

from domain.repository import CustomerRepo
from infrastructure import model


class CustomerRepoImpl(CustomerRepo):
    def __init__(self, db):
        self.db = db

    def create_customer(self, contact: str):
        customer = model.Customer(contact=contact, created_at=datetime.utcnow())
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def get_customer_by_id(self, customer_id):
        customer = self.db.query(model.Customer).filter(model.Customer.customer_id == customer_id).first()
        return customer

    def get_customer_by_contact(self, contact):
        customer = self.db.query(model.Customer).filter(model.Customer.contact == contact).first()
        return customer

    def get_all_customers(self):
        customers = self.db.query(model.Customer).all()
        return customers

    def update_customer(self, customer_id, request):
        customer_query = self.db.query(model.Customer).filter(model.Customer.customer_id == customer_id)
        customer_query.update(request)
        self.db.commit()
        return customer_query.first()

    def delete_customer(self, customer_id):
        customer = self.db.query(model.Customer).filter(model.Customer.customer_id == customer_id).first()
        self.db.delete(customer)
        self.db.commit()
