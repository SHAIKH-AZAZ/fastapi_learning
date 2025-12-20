from typing import ClassVar
from rich.table import Table
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel

class ShipmentStatus(str , Enum):
    placed = "placed"
    in_transit = "in transit"
    out_for_delivery = "out for delivery"
    delivered = "delivered"
    shipping="shipping"
    shipped="shipped"
    processing = "processing"


class Shipment(SQLModel, table=True):
    __tablename__: ClassVar[str]  = "shipment"

    # Primary key with default values  will be assigned and increased automatically 
    id: int = Field(default=None ,primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime 
