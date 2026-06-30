from fastapi import FastAPI
from app.config.settings import settings
from app.routers import health

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for OCR-based document processing and validation.",
    version="1.0.0"
)

app.include_router(health.router)