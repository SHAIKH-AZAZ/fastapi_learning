from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel , Field
from app.Database.models import Seller, ShipmentStatus



class BaseShipment(BaseModel):
    content:str
    weight:float = Field(le=25)
    destination: int

class ShipmentRead(BaseShipment):
    id: UUID
    seller : Seller
    status: ShipmentStatus
    estimated_delivery:datetime
    


class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    content: Optional[str] = None
    weight: Optional[float] = Field(default=None, le=25)
    destination: Optional[int] = None
    status: Optional[ShipmentStatus] = None
    estimated_delivery: Optional[datetime] = None