from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, asin


def haversine(lat1, lon1, lat2, lon2):
    lat1 = float(lat1)
    lat2 = float(lat2)
    lon1 = float(lon1)
    lon2 = float(lon2)
    R = 6371  # Earth radius in kilometers

    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)

    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c  # distance in km


otp_store = {}


def save_otp(contact: str, otp: str):
    otp_store[contact] = {"otp": otp, "expires_at": datetime.utcnow() + timedelta(minutes=5)}


def send_sms(contact: str, otp: str):
    pass


def verify(contact: str, customer_otp: str):
    if not otp_store.get(contact):
        return False
    if datetime.utcnow() > otp_store.get(contact)["expires_at"]:
        del otp_store[contact]
        return False
    if customer_otp == otp_store.get(contact)["otp"]:
        del otp_store[contact]
        return True
    return False
