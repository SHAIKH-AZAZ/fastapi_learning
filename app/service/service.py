import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.Database.models import Shipment, ShipmentStatus
from app.api.schema.shipment import ShipmentUpdate
from app.main import ShipmentCreate
from sqlalchemy.exc import NoResultFound


class ShipmentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: int) -> Shipment:
        shipment = await self.session.get(Shipment, id)
        if shipment is None:
            raise NoResultFound(f"Shipment {id} not found")
        return shipment
        

    async def add(self, shipment_create: ShipmentCreate) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.datetime.now() + datetime.timedelta(days=3),
        )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment

    async def update(self,id:int, shipment_update: ShipmentUpdate) -> Shipment :
        shipment = await self.get(id)
        shipment.sqlmodel_update(shipment_update)

        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    async def delete(self, id: int):
        shipment = await self.get(id)
        await self.session.delete(shipment)
        await self.session.commit()
