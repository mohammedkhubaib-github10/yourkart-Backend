from domain.exception.domain_exception import DomainException


class CartNotFound(DomainException):
    def __init__(self):
        super().__init__(f"Cart not found")


class CartAlreadyExists(DomainException):
    def __init__(self):
        super().__init__(f"Cart already exists")


class CartItemsNotFound(DomainException):
    def __init__(self):
        super().__init__(f"Empty Cart, Cart Items does not Exist")


class CartItemsOfDifferentVendor(DomainException):
    def __init__(self):
        super().__init__(f"Can't Add the Products of Different Vendors")
