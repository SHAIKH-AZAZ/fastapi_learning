from typing import TypeAlias
from uuid import UUID
from typing_extensions import Annotated
from app.Database.models import DeliveryPartner, Seller
from app.Database.redis import is_jti_blacklisted
from app.Database.session import get_session
from app.core.security import oauth2_scheme_seller, oauth2_scheme_partner
from app.service.seller import SellerService
from app.service.shipment import DeliveryPartnerService, ShipmentService
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.shipment_event import ShipmentEventService
from app.utils import decode_access_token

SessionDep: TypeAlias = Annotated[AsyncSession, Depends(get_session)]


# Shipment Service Dependency
def get_shipment_service(session: SessionDep):
    return ShipmentService(
        session,
        DeliveryPartnerService(session),
        ShipmentEventService(session),
    )


# Seller Service Dependency Type
def get_seller_service(session: SessionDep):
    return SellerService(session)


# Delivery Partner Service Dependency Type
def get_delivery_partner_service(session: SessionDep):
    return DeliveryPartnerService(session)


### Access Token Dependency Data fetching can be done in the route itself
async def _get_access_token_data(token: str):
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token Request",
        )
    return data


### seller access token data
async def get_seller_access_token_data(
    token: Annotated[
        str,
        Depends(oauth2_scheme_seller),
    ],
) -> dict:
    return await _get_access_token_data(token)


### partner access token data
async def get_partner_access_token_data(
    token: Annotated[
        str,
        Depends(oauth2_scheme_partner),
    ],
) -> dict:
    return await _get_access_token_data(token)


### LoggedIn seller
async def get_current_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token_data)],
    session: SessionDep,
):
    seller = await session.get(Seller, UUID(token_data["user"]["id"]))
    if seller is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized",
        )
    return


### LoggedIn partner
async def get_current_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token_data)],
    session: SessionDep,
):
    partner = await session.get(DeliveryPartner, UUID(token_data["user"]["id"]))
    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized",
        )
    return partner


### SELLER DEP
SellerDep = Annotated[Seller, Depends(get_current_seller)]

### PARTNER DEP
PartnerDep = Annotated[DeliveryPartner, Depends(get_current_partner)]

# Shipment ServiceDep
ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]

# Seller ServiceDep
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]

# DeliverPartner ServiceDep
PartnerServiceDep = Annotated[DeliveryPartner, Depends(get_current_partner)]

DeliveryPartnerServiceDep = Annotated[
    DeliveryPartnerService, Depends(get_delivery_partner_service)
]
