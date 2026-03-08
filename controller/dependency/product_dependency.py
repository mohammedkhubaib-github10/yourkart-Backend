from fastapi import Depends
from sqlalchemy.orm import Session

from infrastructure.database.session import get_db
from infrastructure.repository import ProductRepoImpl
from service import ProductService


def get_product_repo(db: Session = Depends(get_db)):
    return ProductRepoImpl(db)


def get_product_service(
        repo: ProductRepoImpl = Depends(get_product_repo)
):
    return ProductService(repo)
