from fastapi import Depends
from sqlalchemy.orm import Session

from infrastructure.database.session import get_db
from infrastructure.repository import VendorAddressRepoImpl
from service import VendorAddressService


def get_vendor_address_repo(db: Session = Depends(get_db)):
    return VendorAddressRepoImpl(db)


def get_vendor_address_service(
        repo: VendorAddressRepoImpl = Depends(get_vendor_address_repo)
):
    return VendorAddressService(repo)
