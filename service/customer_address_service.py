from domain.exception import CustomerAddressNotFound
from domain.repository import CustomerAddressRepo


class CustomerAddressService:

    def __init__(self, repo: CustomerAddressRepo):
        self.repo = repo

    def add_address(self, customer_id, request):
        address = self.repo.add_address(customer_id, request)
        return address

    def get_addresses(self, customer_id):
        addresses = self.repo.get_addresses(customer_id)
        if not addresses:
            raise CustomerAddressNotFound()
        return addresses

    def get_address_by_id(self, customer_id, address_id):
        address = self.repo.get_address_by_id(customer_id, address_id)
        if not address:
            raise CustomerAddressNotFound()
        return address

    def update_address(self, customer_id, address_id, request):
        try:
            self.get_address_by_id(customer_id, address_id)
            updated_address = self.repo.update_address(customer_id, address_id, request)
            return updated_address
        except CustomerAddressNotFound:
            raise CustomerAddressNotFound()

    def delete_address(self, customer_id, address_id):
        try:
            self.get_address_by_id(customer_id, address_id)
            self.repo.delete_address(customer_id, address_id)
        except CustomerAddressNotFound:
            raise CustomerAddressNotFound()
