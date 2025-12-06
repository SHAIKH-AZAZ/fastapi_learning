from dataclasses import field
from typing import Any
import string
from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from schema import Shipment 

shipments = {
    1234: {"weight": 1.2, "content": "glassware", "status": "shipping"},
    1235: {"weight": 2.5, "content": "electronics", "status": "delivered"},
    1236: {"weight": 0.8, "content": "documents", "status": "in transit"},
    1237: {"weight": 5.0, "content": "furniture", "status": "processing"},
    1238: {"weight": 1.5, "content": "books", "status": "shipped"},
    1239: {"weight": 3.2, "content": "clothing", "status": "out for delivery"},
    1240: {"weight": 0.5, "content": "accessories", "status": "delivered"},
}

app = FastAPI()


@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, int | str | float]:
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
    return shipments[id]


@app.post("/shipment")
def create_shipement(body : Shipment) -> dict[str, int]:

    if body.weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Weight Greater than 25 Kg is not acceptable ",
        )

    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {"weight": body.weight, "content": body.content, "status": "placed"}
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
def update_shipment(id: int, content: str, weight: float, status: str):
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


@app.patch("/shipment")
def patch_shipment(
    id: int,
    body : dict[str , Any]
):
    shipment = shipments[id]
    # if content:
    #     shipment["content"] = content
    # if weight:
    #     shipment["weight"] = weight
    # if status:
    #     shipment["status"] = status
    
    shipment.update(body)
    shipments[id] = shipment
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
