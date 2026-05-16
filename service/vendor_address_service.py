from domain.exception import VendorAddressNotFound
from domain.repository import VendorAddressRepo


class VendorAddressService:

    def __init__(self, repo: VendorAddressRepo):
        self.repo = repo

    def add_address(self, vendor_id, request):
        address = self.repo.add_address(vendor_id, request)
        return address

    def get_addresses(self, vendor_id):
        addresses = self.repo.get_addresses(vendor_id)
        if not addresses:
            raise VendorAddressNotFound()
        return addresses

    def get_address_by_id(self, vendor_id, address_id):
        address = self.repo.get_address_by_id(vendor_id, address_id)
        if not address:
            raise VendorAddressNotFound()
        return address

    def update_address(self, vendor_id, address_id, request):
        try:
            self.get_address_by_id(vendor_id, address_id)
            updated_address = self.repo.update_address(vendor_id, address_id, request)
            return updated_address
        except VendorAddressNotFound:
            raise VendorAddressNotFound()

    def delete_address(self, vendor_id, address_id):
        try:
            self.get_address_by_id(vendor_id, address_id)
            self.repo.delete_address(vendor_id, address_id)
        except VendorAddressNotFound:
            raise VendorAddressNotFound()
