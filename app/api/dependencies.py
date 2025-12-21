from typing import Annotated, Type , TypeAlias
from app.Database.session import SessionDep, get_session
from app.service.service import ShipmentService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


SessionDep: TypeAlias = Annotated[AsyncSession , Depends(get_session)]


def get_shipment_service(session: SessionDep):
    return ShipmentService(session)


ServiceDep = Annotated[ShipmentService , Depends(get_shipment_service)]