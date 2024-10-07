from __future__ import annotations
from pydantic import BaseModel


class CartRequest(BaseModel):
    item_id: int

