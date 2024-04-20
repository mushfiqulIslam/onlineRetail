from fastapi import APIRouter

bot_router = APIRouter()


@bot_router.get("/")
async def root():
    return {"message": "Hello World"}


@bot_router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}