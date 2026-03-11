from domain.exception import PaymentFailure
from domain.repository import PaymentRepo


class PaymentService:
    def __init__(self, repo: PaymentRepo):
        self.repo = repo

    def make_payment(self, order):
        status = self.repo.make_payment()
        if not status:
            raise PaymentFailure()

