from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "OCR Document Processing API"

    DATABASE_URL: str

    UPLOAD_FOLDER: str

    MAX_FILE_SIZE: int

    OCR_CONFIDENCE_THRESHOLD: float

    POPPLER_PATH: str

    TESSERACT_PATH: str

    class Config:
        env_file = ".env"


settings = Settings()