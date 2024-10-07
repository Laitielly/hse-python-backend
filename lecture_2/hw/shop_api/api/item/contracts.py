from pydantic import BaseModel


class ItemRequest(BaseModel):
    name: str
    price: float