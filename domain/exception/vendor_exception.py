from . import DomainException


class VendorNotFound(DomainException):
    def __init__(self):
        super().__init__(f"Vendor not found")


class VendorAlreadyExists(DomainException):
    def __init__(self):
        super().__init__(f"Vendor already exists")
