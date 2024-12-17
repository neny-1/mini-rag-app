from fastapi import FastAPI
from routes import base,data
from helper.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# when app start up =>event in fastapi =>start connection
@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client=app.mongo_conn[settings.MONGODB_DATABASE]

# when app shutdown =>close connection
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()

app.include_router(base.base_router)
app.include_router(data.data_router)