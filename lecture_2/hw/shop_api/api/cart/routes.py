from http import HTTPStatus
from fastapi import APIRouter, Response 

from lecture_2.hw.shop_api.store import (
    Cart,
    generate_new_cart
)

router = APIRouter(prefix="/cart")

@router.post(
    "/",
    responses={
        HTTPStatus.CREATED: {
            "description": "Successfully created new empty cart",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to created new empty cart. Something went wrong",
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=Cart,
)
async def create_cart(response: Response) -> Cart:
    cart = generate_new_cart()
    response.headers["location"] = f"/cart/{cart.id}"

    return cart
