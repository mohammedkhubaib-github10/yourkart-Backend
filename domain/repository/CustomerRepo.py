from abc import ABC, abstractmethod


class CustomerRepo(ABC):
    @abstractmethod
    def create_customer(self, contact: str):
        pass

    @abstractmethod
    def get_customer_by_id(self, customer_id):
        pass

    @abstractmethod
    def get_customer_by_contact(self, contact):
        pass

    @abstractmethod
    def get_all_customers(self):
        pass

    @abstractmethod
    def update_customer(self, customer_id, request):
        pass

    @abstractmethod
    def delete_customer(self, customer_id):
        pass
