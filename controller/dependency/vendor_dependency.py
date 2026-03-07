from fastapi import Depends
from sqlalchemy.orm import Session

from service import VendorService
from infrastructure.database.session import get_db
from infrastructure.repository import VendorRepoImpl


def get_vendor_repo(db: Session = Depends(get_db)):
    return VendorRepoImpl(db)


def get_vendor_service(
        repo: VendorRepoImpl = Depends(get_vendor_repo)
):
    return VendorService(repo)
