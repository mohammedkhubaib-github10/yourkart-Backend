from fastapi import Depends
from sqlalchemy.orm import Session

from infrastructure.database.session import get_db
from infrastructure.repository import CustomerAddressRepoImpl
from service import CustomerAddressService


def get_customer_address_repo(db: Session = Depends(get_db)):
    return CustomerAddressRepoImpl(db)


def get_customer_address_service(
        repo: CustomerAddressRepoImpl = Depends(get_customer_address_repo)
):
    return CustomerAddressService(repo)
