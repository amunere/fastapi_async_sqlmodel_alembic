from datetime import datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def create_access_token(subject: str | Any, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}

    return jwt.encode(
        payload=to_encode,
        key=settings.ENCRYPT_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

def create_refresh_token(subject: str | Any, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}

    return jwt.encode(
        payload=to_encode,
        key=settings.ENCRYPT_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        jwt=token,
        key=settings.ENCRYPT_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)