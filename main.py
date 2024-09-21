from fastapi import FastAPI
from auth_routh import router as auth_router
from routers import router as note_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(note_router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to FastApi with Authentication"}
