from datetime import datetime, timedelta
from datetime import timezone
import jwt
from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError
from uuid import uuid4

from app.config import security_settings


def generate_access_token(
    data: dict, expiry: timedelta = timedelta(days=security_settings.JWT_TOKEN_EXPIRE)
) -> str:
    return jwt.encode(
        payload={
            **data,
            "jti": str(uuid4().hex),
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET_KEY,
    )


def decode_access_token(token: str) -> dict | None:
    if not token or token.count(".") != 2:
        return None
    
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        return None
    
    