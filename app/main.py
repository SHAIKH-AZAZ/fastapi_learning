from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta
from sqlmodel import Session
from starlette.types import HTTPExceptionHandler
from Database.models import Shipment
from Database.session import SessionDep, create_db_tables
from schema import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
    ShipmentStatus,
)
from dataclasses import field
from typing import Any
from fastapi import Depends, FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(
    lifespan=lifespan_handler,
)


@app.get("/shipment", response_model=ShipmentRead)
async def get_shipment(id: int, session: SessionDep):
    shipment = await session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id does't exists"
        )
    return shipment


#### Create a new shipment with content and weight
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, int]:
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return {"id": new_shipment.id}


# update shipment data with body
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    # update data with give field
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No Data provided to update"
        )
    shipment = session.get(Shipment , id)
    shipment.sqlmodel_update(update)
    
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    
    return shipment



@app.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str , str] :
    # remove from dateabse 
    session.delete(session.get(Shipment , id))
    session.commit()

    return {"detail" : f"Shipment with id #{id} is deleted "}




# scaler API documentations
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
