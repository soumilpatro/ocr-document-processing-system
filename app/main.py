from fastapi import FastAPI

from app.database.database import Base, engine

# Models
from app.models import *

# Routers
from app.routers.documents import router as document_router
from app.routers.validation_router import router as validation_router

# Global Exception Handler
from app.error_handler import register_exception_handlers

# ---------------------------------
# Create Database Tables
# ---------------------------------

Base.metadata.create_all(bind=engine)

# ---------------------------------
# FastAPI App
# ---------------------------------

app = FastAPI(
    title="OCR Document Processing System",
    version="1.0.0",
)

register_exception_handlers(app)

# ---------------------------------
# Routers
# ---------------------------------

app.include_router(document_router)
app.include_router(validation_router)

# ---------------------------------
# Home
# ---------------------------------

@app.get("/")
def home():
    return {
        "message": "OCR Document Processing System"
    }