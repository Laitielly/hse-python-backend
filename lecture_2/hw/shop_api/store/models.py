from __future__ import annotations
from dataclasses import field
from pydantic import BaseModel
from typing import List

from lecture_2.hw.shop_api.api.item.contracts import (
    ItemRequest
)


class Item(BaseModel):
    id: int
    name: str
    price: float
    deleted: bool = False

    @staticmethod
    def from_request(id: int, request: ItemRequest) -> Item:
        new_item = Item(id=id, name=request.name,
                        price=request.price)

        return new_item

class CartItem(BaseModel):
    id: int
    item_name: str
    quantity: int
    available: bool

    model_config = {
        'ignored_types': (dict,)
    }

    @staticmethod
    def from_item(item: Item) -> CartItem:
        return CartItem(
            id = item.id,
            item_name = item.name,
            quantity = 1,
            available = True
        )

class Cart(BaseModel):
    id: int
    items: List[CartItem] = field(default_factory=list)
    price: float = 0.0

    @staticmethod
    def from_id(id: int) -> Cart:
        return Cart(id=id)
