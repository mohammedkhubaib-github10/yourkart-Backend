from abc import ABC, abstractmethod


class CustomerAddressRepo(ABC):
    @abstractmethod
    def add_address(self, customer_id, request):
        pass

    @abstractmethod
    def get_addresses(self, customer_id):
        pass

    @abstractmethod
    def get_address_by_id(self, address_id):
        pass

    @abstractmethod
    def update_address(self, address_id, request):
        pass

    @abstractmethod
    def delete_address(self, address_id):
        pass
