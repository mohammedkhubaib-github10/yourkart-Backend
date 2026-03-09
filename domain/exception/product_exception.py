from domain.exception.domain_exception import DomainException


class ProductNotFound(DomainException):
    def __init__(self):
        super().__init__(f"Product not found")
