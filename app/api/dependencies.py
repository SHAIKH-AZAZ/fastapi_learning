from typing import TypeAlias
from uuid import UUID
from typing_extensions import Annotated
from app.Database.models import Seller
from app.Database.redis import is_jti_blacklisted
from app.Database.session import get_session
from app.core.security import oauth2_scheme
from app.service.seller import SellerService
from app.service.shipment import ShipmentService
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import decode_access_token

SessionDep: TypeAlias = Annotated[AsyncSession, Depends(get_session)]


# Shipment Service Dependency
def get_shipment_service(session: SessionDep):
    return ShipmentService(session)


# Seller Service Dependency Type
def get_seller_service(session: SessionDep):
    return SellerService(session)


### Access Token Dependency Data fetching can be done in the route itself
async def get_access_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token Request",
        )
    return data


### LoggedIn seller
async def get_current_seller(
    token_data: Annotated[str, Depends(get_access_token_data)],
    session: SessionDep,
):
        return await session.get(Seller, UUID(token_data["user"]["id"]))

### SELLER DEP
SellerDep =Annotated[Seller  , Depends(get_current_seller)]


# Shipment ServiceDep
ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]

# Seller ServiceDep
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]
