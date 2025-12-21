from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException,status

from app.Database.models import ShipmentStatus
from app.Database.session import SessionDep, Shipment
from app.api.schema.shipment import ShipmentCreate, ShipmentRead
from app.service.service import ShipmentService



router = APIRouter()

@router.get("/shipment", response_model=ShipmentRead)
async def get_shipment(id: int, session: SessionDep):
    shipment = await ShipmentService(session).get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id does't exists"
        )
    return shipment


#### Create a new shipment with content and weight
@router.post("/shipment")
async def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> Shipment:
    return await ShipmentService(session).add(shipment) 


# update shipment data with body
@router.patch("/shipment", response_model=ShipmentRead)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    # update data with give field
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No Data provided to update"
        )
    
    shipment = await ShipmentService(session).update(shipment_update)
    
    return shipment



@router.delete("/shipment")
async def delete_shipment(id: int, session: SessionDep) -> dict[str , str] :
    # remove from dateabse 
    await ShipmentService(session).delete(id)

    return {"detail" : f"Shipment with id #{id} is deleted "}


