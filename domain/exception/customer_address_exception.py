from domain.exception.domain_exception import DomainException


class CustomerAddressNotFound(DomainException):
    def __init__(self):
        super().__init__(f"Customer Address not found")

