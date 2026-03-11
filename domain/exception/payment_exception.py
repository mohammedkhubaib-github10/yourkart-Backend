from domain.exception.domain_exception import DomainException


class PaymentFailure(DomainException):
    def __init__(self):
        super().__init__(f"Payment has Failed")
