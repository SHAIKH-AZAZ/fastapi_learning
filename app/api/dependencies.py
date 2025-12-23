from typing import TypeAlias
from typing_extensions import Annotated
from app.Database.session import  get_session 
from app.service.seller import SellerService
from app.service.shipment import ShipmentService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

SessionDep: TypeAlias = Annotated[AsyncSession, Depends(get_session)]

# Shipment Service Dependency
def get_shipment_service(session: SessionDep):
    return ShipmentService(session)


# Seller Service Dependency Type 
def get_seller_service(session : SessionDep):
    return SellerService(session)

# Shipment ServiceDep
ShipmentServiceDep = Annotated[ShipmentService , Depends(get_shipment_service)]

# Seller ServiceDep
SellerServiceDep = Annotated[SellerService , Depends(get_seller_service)]