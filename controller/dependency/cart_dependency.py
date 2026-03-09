from fastapi import Depends
from sqlalchemy.orm import Session

from infrastructure.database.session import get_db
from infrastructure.repository import CartRepoImpl
from service import CartService


def get_cart_repo(db: Session = Depends(get_db)):
    return CartRepoImpl(db)


def get_cart_service(
        repo: CartRepoImpl = Depends(get_cart_repo)
):
    return CartService(repo)
