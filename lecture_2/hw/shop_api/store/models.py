from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import List


class CartItem(BaseModel):
    item_id: int
    item_name: str
    num: int
    available: bool

    model_config = {
        'ignored_types': (dict,)
    }

class Cart(BaseModel):
    id: int
    items: List[CartItem] = field(default_factory=list)
    price: float

class Item(BaseModel):
    id: int
    name: str
    price: float
    deleted: bool = False
