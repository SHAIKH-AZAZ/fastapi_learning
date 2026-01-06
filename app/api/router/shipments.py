from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.Database.session import Shipment
from app.api.dependencies import PartnerServiceDep, SellerDep, ShipmentServiceDep
from app.api.schema.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate


router = APIRouter(prefix="/shipment", tags=["Shipment"])


@router.get("/", response_model=ShipmentRead)
async def get_shipment(
    id: UUID,
    service: ShipmentServiceDep,
    _: SellerDep,
) -> Shipment:
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does't exists",
        )
    return shipment


#### Create a new shipment with content and weight
@router.post("/")
async def submit_shipment(
    shipment: ShipmentCreate,
    service: ShipmentServiceDep,
    seller: SellerDep,
) -> Shipment:
    return await service.add(
        shipment,
        seller,
    )


# update shipment data with body
@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    id: UUID,
    shipment_update: ShipmentUpdate,
    partner: PartnerServiceDep,
    service: ShipmentServiceDep,
):
    # update data with give field
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Data provided to update",
        )

    shipment = await service.update(
        id,
        shipment_update,
        partner,
    )

    return shipment


@router.get("/cancel" , response_model=ShipmentRead)
async def cancel_shipment(
    id: UUID,
    seller: SellerDep,
    service: ShipmentServiceDep,
) :
    # remove from database
    shipment =  await service.cancel(id , seller)
    return shipment
    