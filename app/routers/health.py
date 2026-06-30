from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "OCR Document Processing API is running successfully."
    }