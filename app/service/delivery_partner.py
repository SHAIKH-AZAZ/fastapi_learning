from ast import Del
from typing import Sequence
from fastapi import HTTPException, status
from sqlmodel import select
from app.Database.models import DeliveryPartner, Shipment
from app.api.schema.deliver_partner import DeliveryPartnerCreate, DeliveryPartnerUpdate
from app.service.user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session):
        super().__init__(DeliveryPartner, session)

    async def add(self, delivery_partner: DeliveryPartnerCreate):
        return await self._add_user(delivery_partner.model_dump())

    async def get_partner_by_zipcode(self, zipcode: int) -> Sequence[DeliveryPartner]:
        result = await self.session.scalars(
            select(DeliveryPartner).where(
                DeliveryPartner.serviceable_zip_codes.any(zipcode)
            )
        )
        return result.all()

    async def assign_shipment(self, shipment: Shipment):
        eligible_partners = await self.get_partner_by_zipcode(shipment.destination)

        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                shipment.delivery_partner_id = partner.id
                return partner
        
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="No Delivery Partner available for this zipcode",
        )

    async def token(self, email, password):
        return await self._generate_token(email, password=password)

    async def update(self, partner: DeliveryPartner , partner_update : DeliveryPartnerUpdate,):
        data = partner_update.model_dump(exclude_none=True)
        for k , v  in data.items():
            setattr(partner , k  ,v)
        
        await self.session.commit()
        await self.session.refresh(partner)
        return partner
