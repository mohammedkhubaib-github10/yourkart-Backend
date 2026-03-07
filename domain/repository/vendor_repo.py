from abc import ABC, abstractmethod


class VendorRepo(ABC):

    @abstractmethod
    def create_vendor(self, contact: str):
        pass

    @abstractmethod
    def get_vendor_by_id(self, vendor_id):
        pass

    @abstractmethod
    def get_vendor_by_contact(self, contact):
        pass

    @abstractmethod
    def get_all_vendors(self):
        pass

    @abstractmethod
    def update_vendor(self, vendor_id, request):
        pass

    @abstractmethod
    def delete_vendor(self, vendor_id):
        pass
