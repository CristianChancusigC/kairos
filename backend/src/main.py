from fastapi import FastAPI

from src.adapters.inbound.http.health_router import router as health_router
from src.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(health_router, prefix=settings.api_v1_prefix)