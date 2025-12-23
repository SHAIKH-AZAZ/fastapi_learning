from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.dependencies import SellerServiceDep
from app.api.schema.seller import SellerCreate, SellerRead


router = APIRouter(prefix="/seller" , tags=["Seller"])



### Register Seller
@router.post("/signup" , response_model=SellerRead)
async def register_seller(
    seller: SellerCreate,
    service: SellerServiceDep,
):
    return await service.add(seller)


@router.post("/token")
async def login_seller(request_form : Annotated[OAuth2PasswordRequestForm , Depends()] , ):
    request_form.password
    