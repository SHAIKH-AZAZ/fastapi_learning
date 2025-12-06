from typing import Any
import string
from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference

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


@app.get("/shipment/latest")
def get_latast_shipment():
    id = max(shipments.keys())
    return shipments[id]


@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, str | int | float]:

    if id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="details are not found "
        )

    if not id:
        id = max(shipments.keys())
        return shipments[id]
    if id not in shipments:
        return {"status": 404, "detail": "shipment id not found"}
    return shipments[id]


# post request
@app.post("/shipment")
def submit_shipment(weight: float, content: str) -> dict[str, int]:
    if weight > 25:
        raise HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE,
            detail="weight is greater than 25 Kg please check another item ",
        )

    unique_id = max(shipments.keys()) + 1

    shipments[unique_id] = {"content": content, "weight": weight, "status": "placed"}
    return {"id": unique_id}


@app.post("/shipment2")
def submit_shipment2(data: dict[str, Any]) -> dict[str, Any]:
    content = data["content"]
    weigth = data["weight"]
    return {"success": 1}


@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    return {field: shipments[id][field]}


# scaler API documentations
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
