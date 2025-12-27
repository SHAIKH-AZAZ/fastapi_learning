from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.Database.redis import add_jti_to_blacklist
from app.api.dependencies import PartnerServiceDep, get_partner_access_token_data
from app.api.schema.deliver_partner import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerUpdate,
)

router = APIRouter(prefix="/partner", tags=["Partner"])


### Register Delivery Partner
@router.post(
    "/signup",
    response_model=DeliveryPartnerRead,
)
async def register_delivery_partner(
    seller: DeliveryPartnerCreate,
    service,
):
    return await service.add(seller)


@router.post("/token")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "bearer",
    }


### Update the Delivery Partner details
@router.post("/")
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: PartnerServiceDep,
    service,
):
    pass


### Logout Delivery Partner
@router.get("/logout")
async def delivery_partner_logout(
    token_data: Annotated[dict, Depends(get_partner_access_token_data)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"message": "Logout successful"}
