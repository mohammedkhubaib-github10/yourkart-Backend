from domain.exception.domain_exception import DomainException


class VendorAddressNotFound(DomainException):
    def __init__(self):
        super().__init__(f"Vendor Address not found")

