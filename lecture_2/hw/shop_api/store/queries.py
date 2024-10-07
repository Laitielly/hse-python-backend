from typing import Iterable

from lecture_2.hw.shop_api.store.models import (
    Cart,
    # PokemonEntity,
    # PokemonInfo,
)
from lecture_2.hw.shop_api.store.db import (
    _cart,
    _item
)


def int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1


_id_generator = int_id_generator()


def generate_new_cart() -> Cart:
    _id = next(_id_generator)
    new_cart = Cart(id=_id)
    _cart[_id] = new_cart

    return new_cart


# def delete(id: int) -> None:
#     if id in _data:
#         del _data[id]


# def get_one(id: int) -> PokemonEntity | None:
#     if id not in _data:
#         return None

#     return PokemonEntity(id=id, info=_data[id])


# def get_many(offset: int = 0, limit: int = 10) -> Iterable[PokemonEntity]:
#     curr = 0
#     for id, info in _data.items():
#         if offset <= curr < offset + limit:
#             yield PokemonEntity(id, info)

#         curr += 1


# def update(id: int, info: PokemonInfo) -> PokemonEntity | None:
#     if id not in _data:
#         return None

#     _data[id] = info

#     return PokemonEntity(id=id, info=info)


# def upsert(id: int, info: PokemonInfo) -> PokemonEntity:
#     _data[id] = info

#     return PokemonEntity(id=id, info=info)


# def patch(id: int, patch_info: PatchPokemonInfo) -> PokemonEntity | None:
#     if id not in _data:
#         return None

#     if patch_info.name is not None:
#         _data[id].name = patch_info.name

#     if patch_info.published is not None:
#         _data[id].published = patch_info.published

#     return PokemonEntity(id=id, info=_data[id])
