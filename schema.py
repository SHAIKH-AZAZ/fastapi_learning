from importlib.resources._functional import contents
from enum import Enum
from random import randint
from pydantic import BaseModel , Field

# declaring Enums for shipments status 
class ShipmentStatus (str , Enum):
    placed = "placed"
    in_transit = "in transit"
    out_for_delivery = "out for delivery"
    delivered = "delivered"
    shipping="shipping"
    shipped="shipped"
    processing = "processing"


class Shipment(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=25)
    status : ShipmentStatus 
    destination: int = Field(randint(11000 , 11999))
    
    
class BaseShipment(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=25)
    destination: int = Field(randint(11000 , 11999))

class ShipmentRead(BaseShipment):
    status : ShipmentStatus 

class ShipmentCreate(BaseShipment):
    pass


class ShipmentUpdate(BaseModel):
    status : ShipmentStatus