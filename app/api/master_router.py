from fastapi import APIRouter
from app.api.router import shipments , seller

master_router = APIRouter()


master_router.include_router(shipments.router)
master_router.include_router(seller.router)