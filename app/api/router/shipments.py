from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.dependencies.models import Dependant

from app.Database.models import ShipmentStatus
from app.Database.session import Shipment, get_session
from app.api.dependencies import SellerDep, ShipmentServiceDep
from app.api.schema.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.service.shipment import ShipmentService


router = APIRouter(prefix="/shipment", tags=["Shipment"])


@router.get("/", response_model=ShipmentRead)
async def get_shipment(
    id: int,
    service: ShipmentServiceDep,
    _ : SellerDep
):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id does't exists"
        )
    return shipment


#### Create a new shipment with content and weight
@router.post("/")
async def submit_shipment(
    shipment: ShipmentCreate, service: ShipmentServiceDep, seller : SellerDep
) -> Shipment:
    return await service.add(shipment ,seller)


# update shipment data with body
@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    id: int,
    shipment_update: ShipmentUpdate,
    service: ShipmentServiceDep,
):
    # update data with give field
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No Data provided to update"
        )

    shipment = await service.update(id, update)

    return shipment


@router.delete("/")
async def delete_shipment(id: int, service: ShipmentServiceDep) -> dict[str, str]:
    # remove from dateable
    await service.delete(id)

    return {"detail": f"Shipment with id #{id} is deleted "}
