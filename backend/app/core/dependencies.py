from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


def get_current_admin(current_user: dict = Depends(get_current_user)):

    if current_user["role_id"] != 1:
        raise HTTPException(
            status_code=403,
            detail="Admins only"
        )

    return current_user


def get_current_customer(current_user: dict = Depends(get_current_user)):

    if current_user["role_id"] != 2:
        raise HTTPException(
            status_code=403,
            detail="Customers only"
        )

    return current_user