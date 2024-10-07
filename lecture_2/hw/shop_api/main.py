from fastapi import FastAPI

from lecture_2.hw.shop_api.api.cart.routes import router as cart_router

app = FastAPI(title="Shop API")

app.include_router(cart_router)