from fastapi import Depends
from sqlalchemy.orm import Session

from service import CustomerService
from infrastructure.database.session import get_db
from infrastructure.repository import CustomerRepoImpl


def get_customer_repo(db: Session = Depends(get_db)):
    return CustomerRepoImpl(db)


def get_customer_service(
        repo: CustomerRepoImpl = Depends(get_customer_repo)
):
    return CustomerService(repo)
