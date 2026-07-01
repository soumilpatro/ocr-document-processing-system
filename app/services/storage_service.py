import os
import shutil
import uuid

from fastapi import UploadFile

from app.config.settings import settings


async def save_uploaded_file(file: UploadFile) -> str:
    """
    Save uploaded file locally and return the saved file path.
    """

    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

    extension = os.path.splitext(file.filename)[1].lower()

    unique_filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(settings.UPLOAD_FOLDER, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path