from typing import Sequence
from fastapi import HTTPException, status
from sqlmodel import select, any_
from app.Database.models import DeliveryPartner, Shipment
from app.api.schema.deliver_partner import DeliveryPartnerCreate
from app.service.user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session):
        super().__init__(DeliveryPartner, session)

    async def add(self, delivery_partner: DeliveryPartnerCreate):
        return await self._add(
            delivery_partner.model_dump(),
        )

    async def get_partner_by_zipcode(self, zipcode: int) -> Sequence[DeliveryPartner]:
        return (
            await self.session.scalars(
                select(DeliveryPartner).where(
                    zipcode in any_(DeliveryPartner.serviceable_zip_codes)
                )
            )
        ).all()

    async def assign_shipment(self, shipment: Shipment):
        eligible_partners = await self.get_partner_by_zipcode(shipment.destination)
        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="No Delivery Partner is available at the moment", 
        )

    async def token(self, email, password):
        return await self._generate_token(email, password=password)

    async def update(self, partner: DeliveryPartner):
        return await self._update(partner)
