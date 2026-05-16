import random

from domain.exception import InvalidOTP, VendorNotFound
from domain.repository import VendorRepo
from .helper import save_otp, send_sms, verify


class VendorService:
    def __init__(self, repo: VendorRepo):
        self.repo = repo

    @staticmethod
    def request_otp(contact):
        otp = str(random.randint(100000, 999999))
        save_otp(contact, otp)
        send_sms(contact, otp)
        return otp

    def verify_otp(self, contact: str, vendor_otp: str):
        result = verify(contact, vendor_otp)

        if not result:
            raise InvalidOTP()

        try:
            vendor = self.get_vendor_by_contact(contact)
            return vendor.vendor_id
        except VendorNotFound:
            vendor = self.repo.create_vendor(contact)
            return vendor.vendor_id

    def get_vendor_by_id(self, vendor_id):
        vendor = self.repo.get_vendor_by_id(vendor_id)
        if not vendor:
            raise VendorNotFound()
        return vendor

    def get_vendor_by_contact(self, contact):
        vendor = self.repo.get_vendor_by_contact(contact)
        if not vendor:
            raise VendorNotFound()
        return vendor

    def get_all_vendors(self):
        return self.repo.get_all_vendors()

    def update_vendor(self, vendor_id, request):
        vendor = self.repo.get_vendor_by_id(vendor_id)
        if not vendor:
            raise VendorNotFound()
        updated_vendor = self.repo.update_vendor(vendor_id, request)
        return updated_vendor

    def delete_vendor(self, vendor_id):
        vendor = self.repo.get_vendor_by_id(vendor_id)
        if not vendor:
            raise VendorNotFound()
        self.repo.delete_vendor(vendor_id)
