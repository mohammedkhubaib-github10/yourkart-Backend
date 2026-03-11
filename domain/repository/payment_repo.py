from abc import ABC, abstractmethod


class PaymentRepo(ABC):
    @abstractmethod
    def make_payment(self):
        pass
