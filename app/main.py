from fastapi import FastAPI
from app.config.settings import settings
from app.database.database import Base, engine
from app.models.document import Document
from app.routers import health
from app.routers import documents

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for OCR-based document processing and validation.",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)
app.include_router(health.router)
app.include_router(documents.router)