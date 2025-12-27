from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from starlette.requests import Request

from app.utils import decode_access_token

oauth2_scheme_seller = OAuth2PasswordBearer(tokenUrl="seller/token")
oauth2_scheme_partner = OAuth2PasswordBearer(tokenUrl="partner/token")


class AccessTokenBearer(HTTPBearer):
    async def __call__(self, request: Request) -> dict:
        auth_credentials: HTTPAuthorizationCredentials | None = await super().__call__(
            request
        )

        if auth_credentials is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authenticated",
            )

        token = auth_credentials.credentials
        token_data = decode_access_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not Authorized",
            )

        return token_data


access_token_bearer = AccessTokenBearer()

Annotated[dict, Depends(access_token_bearer)]
