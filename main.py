
from fastapi import FastAPI
from api import video_router
from db import database, metadata, engine

app = FastAPI()


app.state.database = database
metadata.create_all(engine)

app.include_router(video_router)

@app.on_event("startup")
async def startup():
    database_ = app.state.database
    if not database_.is_connected:
        await database.connect()

@app.on_event("shutdown")
async def shutdown():
    database_ = app.state.database
    if database_.is_connected:
        await database.disconnect()