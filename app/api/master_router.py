from fastapi import APIRouter
from app.api.router import shipments , seller , delivery_partner

master_router = APIRouter()


master_router.include_router(shipments.router)
master_router.include_router(seller.router)
master_router.include_router(delivery_partner.router)