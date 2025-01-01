from fastapi import FastAPI
from routes import base,data,nlp
from helper.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory

app = FastAPI()

# when app start up =>event in fastapi =>start connection
async def startup_db_client():

    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    llm_provider_factory= LLMProviderFactory(settings)
    vectordb_provider_factory =VectorDBProviderFactory(settings)

    # generation client
    app.generation_client= llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)
    
   # embedding client
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)

    #vector db client
    app.vectordb_client= vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
    app.vectordb_client.connect()
# when app shutdown =>close connection
async def shutdown_db_client():
    app.mongo_conn.close()
    app.vectordb_client.disconnect()

#app.router.lifespan.on_startup.append(startup_db_client)
#app.router.lifespan.on_shutdown.append(shutdown_db_client)

app.on_event("startup")(startup_db_client)
app.on_event("shutdown")(shutdown_db_client)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)