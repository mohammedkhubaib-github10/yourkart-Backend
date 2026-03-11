from domain.repository import PaymentRepo


class PaymentRepoImpl(PaymentRepo):
    def __init__(self, db):
        self.db = db

    def make_payment(self):
        pass
