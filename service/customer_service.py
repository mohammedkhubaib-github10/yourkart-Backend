import random

from domain.exception import auth_exception, customer_exception
from domain.repository import CustomerRepo
from .helper import send_sms, save_otp, verify


class CustomerService:
    def __init__(self, repo: CustomerRepo):
        self.repo = repo

    @staticmethod
    def request_otp(contact):
        otp = str(random.randint(10000, 99999))
        save_otp(contact, otp)
        send_sms(contact, otp)
        return otp

    def verify_otp(self, contact: str, customer_otp: str):
        result = verify(contact, customer_otp)

        if not result:
            raise AuthException.InvalidOTP()

        try:
            customer = self.get_customer_by_contact(contact)
            return customer
        except CustomerException.CustomerNotFound:
            customer = self.repo.create_customer(contact)
            return customer

    def get_customer_by_id(self, customer_id):
        customer = self.repo.get_customer_by_id(customer_id)
        if not customer:
            raise CustomerException.CustomerNotFound()
        return customer

    def get_customer_by_contact(self, contact):
        customer = self.repo.get_customer_by_contact(contact)
        if not customer:
            raise CustomerException.CustomerNotFound()
        return customer

    def get_all_customers(self):
        return self.repo.get_all_customers()

    def update_customer(self, customer_id, request):
        customer = self.repo.get_customer_by_id(customer_id)
        if not customer:
            raise CustomerException.CustomerNotFound()
        updated_customer = self.repo.update_customer(customer_id, request)
        return updated_customer

    def delete_customer(self, customer_id):
        customer = self.repo.get_customer_by_id(customer_id)
        if not customer:
            raise CustomerException.CustomerNotFound()
        self.repo.delete_customer(customer_id)
