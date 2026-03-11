from enum import Enum


class PaymentMode(str, Enum):
    DebitCard = "debit_card"
    CreditCard = "credit_card"
    NetBanking = "net_banking"
    UPI = "upi"
    COD = "cod"


class OrderStatus(Enum):
    Failed = "failed"
    Placed = "placed"
    Cancelled = "cancelled"
    Shipped = "shipped"
    Delivered = "delivered"
    Pending = "pending"


class PaymentStatus(str, Enum):
    Success = "success"
    Failed = "failed"
