from fastapi import FastAPI
from routes import base, data
from contextlib import asynccontextmanager
from helpers.database import db
from helpers.factories import get_llm_clients

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    app.db = db.db
    app.generation_client, app.embedding_client = get_llm_clients()
    
    yield
    await db.disconnect()
    
app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)