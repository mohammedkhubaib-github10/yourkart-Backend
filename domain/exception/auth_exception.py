from . import DomainException


class InvalidOTP(DomainException):
    def __init__(self):
        super().__init__("Invalid OTP or OTP expired")


class OTPExpired(DomainException):
    def __init__(self):
        super().__init__("OTP has expired")
