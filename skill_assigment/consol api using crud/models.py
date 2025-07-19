from pydantic import BaseModel, Field
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemInDB(Item):
    id: str = Field(alias="_id")
