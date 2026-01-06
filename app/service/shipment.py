import datetime
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.Database.models import DeliveryPartner, Seller, Shipment, ShipmentStatus
from app.api.schema import shipment
from app.api.schema.shipment import ShipmentCreate, ShipmentUpdate
from sqlalchemy.exc import NoResultFound

from app.service.base import BaseService
from app.service.delivery_partner import DeliveryPartnerService
from app.service.shipment_event import ShipmentEventService


class ShipmentService(BaseService[Shipment]):
    def __init__(
        self,
        session: AsyncSession,
        partner_service: DeliveryPartnerService,
        event_service: ShipmentEventService,
    ):
        super().__init__(Shipment, session)
        self.partner_service = partner_service
        self.event_service = event_service

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
        partner = await self.partner_service.assign_shipment(new_shipment)
        new_shipment.delivery_partner_id = partner.id
        shipment = await self._add(new_shipment)
        event = await self.event_service.add(
            shipment=new_shipment,
            location=seller.zip_code,
            status=ShipmentStatus.placed,
            description=f"Shipment placed by seller {partner.name}",
        )
        shipment.timeline.append(event)
        return shipment

    async def update(
        self,
        id: UUID,
        shipment_update: ShipmentUpdate,
        partner: DeliveryPartner,
    ) -> Shipment:
        shipment = await self.get(id)

        if shipment.delivery_partner_id != partner.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not Authorized to update this shipment",
            )

        update = shipment_update.model_dump(exclude_none=True)
        if shipment_update.estimated_delivery:
            shipment.estimated_delivery = shipment_update.estimated_delivery

        if len(update) > 1 or not shipment_update.estimated_delivery:
            await self.event_service.add(
                shipment=shipment,
                **update,
            )

        return await self._update(shipment)

    async def cancel(self, id: UUID, seller: Seller):
        # validated seller owns the shipment
        shipment = await self.get(id)

        if shipment.seller_id != seller.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not Authorized to cancel this shipment",
            )
        event = await self.event_service.add(
            shipment=shipment,
            status=ShipmentStatus.cancelled,
        )
        shipment.timeline.append(event)
        return await self._update(shipment)

    async def delete(self, id: UUID):
        shipment = await self.get(id)
        if shipment is None:
            raise NoResultFound(f"Shipment {id} not found")

        await self._delete(shipment)
