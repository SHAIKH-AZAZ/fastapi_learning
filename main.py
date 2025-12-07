from schema import ShipmentCreate,ShipmentRead,ShipmentUpdate,Shipment , ShipmentStatus
from enum import Enum
from dataclasses import field
from typing import Any
from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from database import save ,shipments 

# shipments = {
#     1234: {"weight": 1.2, "content": "glassware", "status": "shipping"},
#     1235: {"weight": 2.5, "content": "electronics", "status": "delivered"},
#     1236: {"weight": 0.8, "content": "documents", "status": "in transit"},
#     1237: {"weight": 5.0, "content": "furniture", "status": "processing"},
#     1238: {"weight": 1.5, "content": "books", "status": "shipped"},
#     1239: {"weight": 3.2, "content": "clothing", "status": "out for delivery"},
#     1240: {"weight": 0.5, "content": "accessories", "status": "delivered"},
# }

app = FastAPI()


@app.get("/shipment" , response_model=ShipmentRead)
def get_shipment(id: int | None = None) :
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Id is required for shipment details",
        )

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found in DataBase",
        )
    shipment = shipments[id]
    return Shipment(
        **shipment
    )


@app.post("/shipment")
def create_shipement(shipment : ShipmentCreate) -> dict[str, int]:

    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        **shipment.model_dump(),
        "id":new_id,
        "status": "placed" , 
        }
    save()
    return {"id": new_id}


@app.get("/shipment/{field}")
def get_shipment_details(field: str, id: int) -> str:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="shipment detail not found"
        )
    if field not in shipments[id]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"field not found for {id}"
        )
    return shipments[id][field]


@app.put("/shipment")
def update_shipment(id: int, content: str, weight: float, status: ShipmentStatus):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="shipment details not found "
        )
    if shipments[id]["status"] == "delivered":
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Shipment is already delivered",
        )
    shipments[id] = {"weight": weight, "content": content, "status": status}
    return shipments[id]



@app.patch("/shipment" , response_model=ShipmentRead)
def patch_shipment(
    id: int,
    body : ShipmentUpdate
):
    # update shipment data with body 
    shipments[id].update(body)
    save()
    return shipments[id]

@app.delete("/shipment")
def delete_shipment(id : int):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="shipment not found"
        )
    shipment = shipments.pop(id)
    return {"id" : id , "shipment":shipment}

# scaler API documentations
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
