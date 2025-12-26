from typing import Annotated
from fastapi import Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from starlette.requests import Request

from app.utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="seller/token")

class AccessTokenBearer(HTTPBearer):
    async def __call__(self, request: Request) :
        authCredentials =await super().__call__(request)
        token =authCredentials.credentials 
        token_data = decode_access_token(token)
        
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not Authorized ",
            )
        return token_data
access_token_bearer = AccessTokenBearer()

Annotated[dict , Depends(access_token_bearer)]