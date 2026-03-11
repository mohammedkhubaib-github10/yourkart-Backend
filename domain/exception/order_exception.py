from domain.exception.domain_exception import DomainException


class OrderNotFound(DomainException):
    def __init__(self):
        super().__init__(f"Order not found")


class OrderAlreadyExists(DomainException):
    def __init__(self):
        super().__init__(f"Order already exists")
