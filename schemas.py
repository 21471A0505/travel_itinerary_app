from pydantic import BaseModel
from typing import List, Optional

class ActivitySchema(BaseModel):
    name: str
    description: str

class TransferSchema(BaseModel):
    from_location: str
    to_location: str
    mode: str

class HotelStaySchema(BaseModel):
    hotel_name: str
    address: str

class DaySchema(BaseModel):
    day_number: int
    hotels: List[HotelStaySchema]
    transfers: List[TransferSchema]
    activities: List[ActivitySchema]

class ItineraryCreate(BaseModel):
    name: str
    region: str
    nights: int
    days: List[DaySchema]

class ItineraryOut(BaseModel):
    id: int
    name: str
    region: str
    nights: int

    class Config:
        orm_mode = True
