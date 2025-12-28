import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.Database.models import Seller, Shipment, ShipmentStatus
from app.api.schema.shipment import ShipmentCreate
from sqlalchemy.exc import NoResultFound

from app.service.base import BaseService
from app.service.delivery_partner import DeliveryPartnerService


class ShipmentService(BaseService[Shipment]):
    def __init__(
        self,
        session: AsyncSession,
        partner_service: DeliveryPartnerService,
    ):
        super().__init__(Shipment, session)
        self.partner_service = partner_service

    async def get(self, id: UUID) -> Shipment:
        shipment = await self._get(id)
        if shipment is None:
            raise NoResultFound(f"Shipment {id} not found")

        return shipment

    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.datetime.now() + datetime.timedelta(days=3),
            seller_id=seller.id,
        )
        partner=await self.partner_service.assign_shipment(new_shipment)
        new_shipment.delivery_partner_id = partner.id
        return await self._add(new_shipment)

    async def update(self, id: UUID, shipment_update: dict) -> Shipment:
        shipment = await self.get(id)
        shipment.sqlmodel_update(shipment_update)

        return await self._update(shipment)

    async def delete(self, id: UUID):
        shipment = await self.get(id)
        if shipment is None:
            raise NoResultFound(f"Shipment {id} not found")

        await self._delete(shipment)
