from random import randint
from pydantic import BaseModel , Field

class Shipment(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=25)
    destination: int = Field(default=randint(11000 , 11999))