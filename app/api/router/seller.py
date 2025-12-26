from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.Database.redis import add_jti_to_blacklist
from app.api.dependencies import SellerServiceDep, get_access_token_data
from app.api.schema.seller import SellerCreate, SellerRead

router = APIRouter(prefix="/seller", tags=["Seller"])


### Register Seller
@router.post(
    "/signup",
    response_model=SellerRead,
)
async def register_seller(
    seller: SellerCreate,
    service: SellerServiceDep,
):
    return await service.add(seller)


@router.post("/token")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "bearer",
    }


### Logout Seller
@router.get("/logout")
async def seller_logout(
    token_data: Annotated[dict, Depends(get_access_token_data)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"message": "Logout successful"}