from fastapi import APIRouter

router = APIRouter(
    prefix="/api/health",
    tags=["Health"]
)


@router.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "OCR Document Processing API is running successfully."
    }