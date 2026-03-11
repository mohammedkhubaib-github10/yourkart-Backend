from fastapi import Depends
from sqlalchemy.orm import Session

from controller.dependency.cart_dependency import get_cart_repo
from infrastructure.database.session import get_db
from infrastructure.repository import OrderRepoImpl, CartRepoImpl, PaymentRepoImpl
from service import OrderService
from service.payment_service import PaymentService


def get_order_repo(db: Session = Depends(get_db)):
    return OrderRepoImpl(db)


def get_payment_repo(db: Session = Depends(get_db)):
    return PaymentRepoImpl(db)


def get_payment_service(
        repo: PaymentRepoImpl = Depends(get_payment_repo)
):
    return PaymentService(repo)


def get_order_service(
        repo: OrderRepoImpl = Depends(get_order_repo),
        cart_repo: CartRepoImpl = Depends(get_cart_repo),
        payment_service: PaymentService = Depends(get_payment_service)
):
    return OrderService(repo, cart_repo, payment_service)
