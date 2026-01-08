from typing import List
from pydantic import EmailStr
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import INTEGER, Column
from sqlalchemy.dialects import postgresql
from sqlmodel import DateTime, Field, Relationship, SQLModel
from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import ARRAY


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in transit"
    out_for_delivery = "out for delivery"
    delivered = "delivered"
    shipping = "shipping"
    shipped = "shipped"
    processing = "processing"
    cancelled = "cancelled"


### base user model for creating seller and delivery partners
class User(SQLModel, table=False):

    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
    )

    name: str
    email: EmailStr
    password_hash: str = Field(exclude=True)


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    # Primary key with default values  will be assigned and increased automatically
    id: UUID = Field(
            default_factory=uuid4,
            primary_key=True,
        )

    created_at: datetime  = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )


    content: str
    weight: float = Field(le=25)
    destination: int

    timeline: list["ShipmentEvent"] = Relationship(
        back_populates="shipment",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    estimated_delivery: datetime

    delivery_partner_id: UUID | None = Field(
        default=None,
        foreign_key="delivery_partner.id",
    )

    # check
    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )

    @property
    def status(self):
        return self.timeline[-1].status if len(self.timeline) > 0 else None


class ShipmentEvent(SQLModel, table=True):
    __tablename__ = "shipment_event"

    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
    )
    created_at: datetime | None = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    location: int
    status: ShipmentStatus
    description: str | None = Field(default=None)

    shipment_id: UUID = Field(foreign_key="shipment.id")
    shipment: Shipment = Relationship(
        back_populates="timeline",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )


class Seller(User, table=True):
    __tablename__ = "seller"  # type: ignore

    created_at: datetime | None = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    address: str | None = Field(nullable=True)
    zip_code: int | None = Field(nullable=True)
    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={
            "lazy": "selectin",
        },
    )


class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"  # type: ignore

    created_at: datetime | None = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )

    serviceable_zip_codes: List[int] = Field(
        default_factory=list, sa_column=Column(ARRAY(INTEGER), nullable=True)
    )

    max_handling_capacity: int
    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    @property
    def active_shipment(self):
        return [
            shipment
            for shipment in self.shipments
            if shipment.status != ShipmentStatus.delivered
            if shipment.status != ShipmentStatus.cancelled
        ]

    @property
    def current_handling_capacity(self):
        return max(0, self.max_handling_capacity - len(self.active_shipment))
