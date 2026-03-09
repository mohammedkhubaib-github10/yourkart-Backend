from abc import ABC, abstractmethod


class VendorAddressRepo(ABC):
    @abstractmethod
    def add_address(self, vendor_id, request):
        pass

    @abstractmethod
    def get_addresses(self, vendor_id):
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