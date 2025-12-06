from pydantic import BaseModel

class Shipment(BaseModel):
    content: str 
    weight: float
    destination: int