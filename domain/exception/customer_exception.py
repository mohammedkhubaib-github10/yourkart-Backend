from domain.exception.domain_exception import DomainException


class CustomerNotFound(DomainException):
    def __init__(self):
        super().__init__(f"Customer not found")


class CustomerAlreadyExists(DomainException):
    def __init__(self):
        super().__init__(f"Customer already exists")
