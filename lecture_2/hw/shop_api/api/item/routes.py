from http import HTTPStatus
from fastapi import APIRouter, Response, HTTPException

from lecture_2.hw.shop_api.store import (
    Item,
    generate_new_item,
    get_item_from_id,
    get_items
)
from .contracts import (
    ItemRequest
)
from typing import Optional, List

router = APIRouter(prefix="/item")

@router.post(
    "/",
    responses={
        HTTPStatus.CREATED: {
            "description": "Successfully added new item",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to add new item",
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=Item,
)
async def create_item(item_request: ItemRequest, response: Response) -> Item:
    item = generate_new_item(item_request)
    response.headers["location"] = f"/item/{item.id}"

    return item

@router.get(
    "/{item_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Item,
)
async def get_item(item_id: int) -> Item:
    try:
        item = get_item_from_id(item_id)
    except KeyError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item with this id is not found")
    return item

@router.get(
    "/",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned lists of requested items",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested items",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=List[Item],
)
async def get_list_items(offset: int = 0,
                         limit: int = 10,
                         min_price: Optional[float] = None,
                         max_price: Optional[float] = None,
                         show_deleted: bool = False
                         ) -> List[Item]:
    try:
        list_of_items = get_items(offset,
                                  limit,
                                  min_price,
                                  max_price,
                                  show_deleted)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f"{e}")
    if list_of_items is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Items not found")
    return list_of_items

# @router.post(
#     "/{cart_id}/add/{item_id}",
#     responses={
#         HTTPStatus.CREATED: {
#             "description": "Successfully added item to cart",
#         },
#         HTTPStatus.UNPROCESSABLE_ENTITY: {
#             "description": "Failed to add item to cart",
#         },
#     },
#     status_code=HTTPStatus.CREATED,
#     response_model=Cart,
# )
# async def add_item_to_cart_from_id(cart_id: int, item_id: int) -> Cart:
#     try:
#         cart = add_item_to_cart(cart_id, item_id)
#     except Exception as e:
#         raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
#     return cart
