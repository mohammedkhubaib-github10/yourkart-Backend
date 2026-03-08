from datetime import datetime

from domain.repository import VendorRepo
from infrastructure import model


class VendorRepoImpl(VendorRepo):
    def __init__(self, db):
        self.db = db

    def create_vendor(self, contact: str):
        vendor = model.Vendor(contact=contact, created_at=datetime.utcnow())
        self.db.add(vendor)
        self.db.commit()
        self.db.refresh(vendor)
        return vendor

    def get_vendor_by_id(self, vendor_id):
        vendor = self.db.query(model.Vendor).filter(model.Vendor.vendor_id == vendor_id).first()
        return vendor

    def get_vendor_by_contact(self, contact):
        vendor = self.db.query(model.Vendor).filter(model.Vendor.contact == contact).first()
        return vendor

    def get_all_vendors(self):
        vendors = self.db.query(model.Vendor).all()
        return vendors

    def get_nearby_vendors(self, address_id):
        pass

    def update_vendor(self, vendor_id, request):
        vendor_query = self.db.query(model.Vendor).filter(model.Vendor.vendor_id == vendor_id)
        vendor_query.update(request.model_dump())
        self.db.commit()
        return vendor_query.first()

    def delete_vendor(self, vendor_id):
        vendor = self.db.query(model.Vendor).filter(model.Vendor.vendor_id == vendor_id).first()
        self.db.delete(vendor)
        self.db.commit()
