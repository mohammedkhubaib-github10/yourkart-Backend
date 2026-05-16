from domain.repository import CustomerAddressRepo
from infrastructure import model


class CustomerAddressRepoImpl(CustomerAddressRepo):

    def __init__(self, db):
        self.db = db

    def add_address(self, customer_id, request):
        address = model.CustomerAddress(street=request.street, pincode=request.pincode,
                                        city=request.city, flat_no=request.flat_no, latitude=request.latitude,
                                        longitude=request.longitude,
                                        customer_id=customer_id)
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address

    def get_addresses(self, customer_id):
        addresses = self.db.query(model.CustomerAddress).filter(model.CustomerAddress.customer_id == customer_id).all()
        return addresses

    def get_address_by_id(self, customer_id, address_id):
        address = self.db.query(model.CustomerAddress).filter(model.CustomerAddress.address_id == address_id,
                                                              model.CustomerAddress.customer_id == customer_id).first()
        return address

    def update_address(self, customer_id, address_id, request):
        address_query = self.db.query(model.CustomerAddress).filter(model.CustomerAddress.address_id == address_id,
                                                                    model.CustomerAddress.customer_id == customer_id)
        address = address_query.first()
        address_query.update(request.model_dump())
        self.db.commit()
        self.db.refresh(address)
        return address

    def delete_address(self, customer_id, address_id):
        address_query = self.db.query(model.CustomerAddress).filter(model.CustomerAddress.address_id == address_id,
                                                                    model.CustomerAddress.customer_id == customer_id)
        address = address_query.first()
        self.db.delete(address)
        self.db.commit()
