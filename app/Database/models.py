from typing import ClassVar
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from sqlalchemy import INTEGER, Column, ARRAY
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

    delivery_Partner_id: UUID = Field(
        foreign_key="delivery_partner.id",
    )
    created_at: datetime =Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )
    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )


class User(SQLModel):
    name: str
    email: EmailStr
    password_hash: str = Field(exclude=True)


class Seller(User, table=True):
    __tablename__ = "seller"

    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )
    address: int

    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )


class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"
    id: UUID = Field(
        sa_column=Column(
            postgresql.UUID,
            default=uuid4,
            primary_key=True,
        )
    )

    created_at: datetime =Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    serviceable_zip_codes: list[int] = Field(
        sa_column=Column(ARRAY(INTEGER)),
    )
    max_handling_capacity: int
    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )
