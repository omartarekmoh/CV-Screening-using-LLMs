from fastapi import FastAPI
from routes import base, data
from contextlib import asynccontextmanager
from helpers.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    app.db = db.db
    yield
    await db.disconnect()
    
app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)