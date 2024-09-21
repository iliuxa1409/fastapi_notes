from fastapi import FastAPI
from database import engine, Base
from routers import router

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to FastApi"}
