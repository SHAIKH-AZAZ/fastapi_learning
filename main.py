from schema import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
    Shipment,
    ShipmentStatus,
)
from enum import Enum
from dataclasses import field
from typing import Any
from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from database import Database


app = FastAPI()

db = Database()


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int | None = None):

    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Id is required for shipment details",
        )
    return shipment


@app.post("/shipment")
def create_shipement(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = db.create(shipment)
    return {"id": new_id}




@app.patch("/shipment", response_model=ShipmentRead)
    # update shipment data with body
def patch_shipment(id : int , shipment: ShipmentUpdate):
    shipment = db.update(id , shipment)
    return shipment


@app.delete("/shipment")
def delete_shipment(id: int):
    db.delete(id)

    return {"id": id}


# scaler API documentations
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
