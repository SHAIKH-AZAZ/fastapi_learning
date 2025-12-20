from datetime import datetime
from importlib.resources._functional import contents
from enum import Enum
from random import randint
from pydantic import BaseModel , Field
from Database.models import ShipmentStatus



class BaseShipment(BaseModel):
    content:str
    weight:float = Field(le=25)
    destination: int

class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery:datetime
    


class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseShipment):
    status: ShipmentStatus |None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)