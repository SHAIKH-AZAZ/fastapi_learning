from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BaseSeller(BaseModel):
    name: str
    email: EmailStr

class SellerRead(BaseSeller):
    pass


class SellerCreate(BaseSeller):
    password : str 

class SellerPublic(SellerCreate):
    model_config = {"from_attributes": True}
    
