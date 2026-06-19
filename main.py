from contextlib import asynccontextmanager

import app.database as database
from fastapi import FastAPI
from app.api.routes import audit
from app.logger import get_logger
from app.config import get_settings

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(
    title="AEO Audit Tool",
    description="Audit websites for AI Retrieval readiness",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(audit.router, prefix="/api/v1", tags=["audit"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "env": settings.APP_ENV}
