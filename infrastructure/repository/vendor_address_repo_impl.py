from domain.repository import VendorAddressRepo
from infrastructure import model


class VendorAddressRepoImpl(VendorAddressRepo):

    def __init__(self, db):
        self.db = db

    def add_address(self, vendor_id, request):
        address = model.VendorAddress(street=request.street, pincode=request.pincode,
                                      city=request.city, latitude=request.latitude,
                                      longitude=request.longitude,
                                      vendor_id=vendor_id)
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address

    def get_addresses(self, vendor_id):
        address = self.db.query(model.VendorAddress).filter(model.VendorAddress.vendor_id == vendor_id).all()
        return address

    def get_address_by_id(self, address_id):
        address = self.db.query(model.VendorAddress).filter(model.VendorAddress.address_id == address_id).first()
        return address

    def update_address(self, address_id, request):
        address_query = self.db.query(model.VendorAddress).filter(model.VendorAddress.address_id == address_id)
        address = address_query.first()
        address_query.update(request.model_dump())
        self.db.commit()
        self.db.refresh(address)
        return address

    def delete_address(self, address_id):
        address_query = self.db.query(model.VendorAddress).filter(model.VendorAddress.address_id == address_id)
        address = address_query.first()
        self.db.delete(address)
        self.db.commit()
