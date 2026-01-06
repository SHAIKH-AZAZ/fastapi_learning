from sqlalchemy.ext.asyncio import AsyncSession
from app.Database.models import Shipment , ShipmentEvent , ShipmentStatus
from app.service.base import BaseService


class ShipmentEventService(BaseService[ShipmentEvent]):
    
    def __init__(self,  session: AsyncSession) -> None:
        super().__init__(ShipmentEvent, session)
    
    async def add(
        self,
        shipment: Shipment,
        location: int | None = None,
        status: ShipmentStatus | None = None,
        description: str | None = None,
    ):
        if shipment.id is None:
            raise ValueError("Shipment must be saved before adding events.")
        
        last_event = await self.get_latest_event(shipment)
        
        if last_event is None: 
            if location is None or status is None:
                raise ValueError("First event must have location and status.")
        else:
            # Fallback to last event values if not provided
            location = location if location is not None else last_event.location
            status = status if status is not None else last_event.status

        # Missing: Actually creating and saving the new event
        if description is None:
            description = self._generate_description(status, location)
            
        new_event = ShipmentEvent(
            shipment_id=shipment.id,
            location=location,
            status=status,
            description=description
        )
        self.session.add(new_event)
        await self.session.flush() # Or commit depending on your service pattern
        return new_event
        
    
    async def get_latest_event(self, shipment: Shipment):
    # Fix: Ensure timeline is loaded. Use awaitable_attrs or a fresh query.
    # If not eagerly loaded, you must load it explicitly:
    # await self.session.refresh(shipment, ["timeline"])
    
        timeline = list(shipment.timeline) # Convert to list to avoid side effects
        if not timeline:
            return None
        
        # Correct Syntax: sort(key=...)
        timeline.sort(key=lambda event: event.created_at) 
        return timeline[-1]
    
    def _generate_description(self, status: ShipmentStatus, location: int):
        match status:
            case ShipmentStatus.placed:
                return f"Shipment has been placed at location {location}."
            case ShipmentStatus.delivered:
                return f"Shipment delivered to location {location}."
            case ShipmentStatus.in_transit:
                return f"Shipment in transit at location {location}."
            case ShipmentStatus.out_for_delivery:
                return f"Out for delivery from location {location}."
            case ShipmentStatus.processing:
                return f"Processing at location {location}."
            case ShipmentStatus.shipped:
                return f"Shipped from location {location}."
            case ShipmentStatus.shipping:
                return f"Shipping, currently at location {location}."
            case ShipmentStatus.cancelled:
                return f"Shipment cancelled by seller."
            case _:
                return f"Scanned at location {location}."
