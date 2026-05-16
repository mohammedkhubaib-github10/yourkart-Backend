from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from controller.dependency.customer_dependency import get_customer_service
from controller.dependency.vendor_dependency import get_vendor_service
from service.auth_service import verify_token

security = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        customer_service=Depends(get_customer_service),
        vendor_service=Depends(get_vendor_service)
):
    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    user_id = payload['user_id']
    role = payload['role']
    try:
        if role == 'customer':
            customer_service.get_customer_by_id(user_id)

        else:
            vendor_service.get_vendor_by_id(user_id)
    except:
        raise HTTPException(status_code=404, detail="user not found")

    return payload
