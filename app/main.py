from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
from sqlmodel import Session
from starlette.types import HTTPExceptionHandler
from Database.models import Shipment
from Database.session import SessionDep, create_db_tables
from app.api.schema.shipment import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
    ShipmentStatus,
)
from dataclasses import field
from typing import Any
from fastapi import Depends, FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from app.api.router import router

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(
    lifespan=lifespan_handler,
)

app.include_router(router)


# scaler API documentations
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
