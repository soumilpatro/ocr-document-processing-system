import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from app.services.text_cleanup_service import clean_text
from app.config.settings import settings
pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH



def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """
    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return clean_text(text)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from every page of a PDF.
    """

    pages = convert_from_path(
    pdf_path,
    poppler_path=settings.POPPLER_PATH,
)

    extracted_text = ""

    for page in pages:
        extracted_text += pytesseract.image_to_string(page)
        extracted_text += "\n"

    return clean_text(extracted_text)


def extract_text(file_path: str) -> str:
    """
    Detect file type and perform OCR.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    return extract_text_from_image(file_path)