from typing import ClassVar
from pydantic import EmailStr
from datetime import datetime
from enum import Enum
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in transit"
    out_for_delivery = "out for delivery"
    delivered = "delivered"
    shipping = "shipping"
    shipped = "shipped"
    processing = "processing"


class Shipment(SQLModel, table=True):
    __tablename__: ClassVar[str] = "shipment"

    # Primary key with default values  will be assigned and increased automatically
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime

    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )


class Seller(SQLModel, table=True):

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    name: str

    email: EmailStr
    password_hash: str

    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )
