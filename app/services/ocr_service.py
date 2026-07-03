import os
import time
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from app.services.text_cleanup_service import clean_text
from app.config.settings import settings
from app.services.logging.logger import logger
pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH



def extract_text_from_image(image_path: str) -> str:

    logger.info(f"Starting OCR for image: {image_path}")
    start_time = time.perf_counter()
    try:
        image = Image.open(image_path)

        text = pytesseract.image_to_string(image)
        

        elapsed = time.perf_counter() - start_time
        logger.info(f"Image OCR completed successfully in {elapsed:.2f} seconds.")
        return clean_text(text)

    except Exception as e:
        logger.error(f"Image OCR failed: {str(e)}")
        raise

def extract_text_from_pdf(pdf_path: str):

    logger.info(f"Starting OCR for PDF: {pdf_path}")
    start_time = time.perf_counter()
    try:

        pages = convert_from_path(
            pdf_path,
            poppler_path=settings.POPPLER_PATH,
        )

        logger.info(f"Converted PDF into {len(pages)} pages.")

        extracted_text = ""

        for page in pages:
            extracted_text += pytesseract.image_to_string(page)
            extracted_text += "\n"

        elapsed = time.perf_counter() - start_time
        logger.info(f"PDF OCR completed successfully in {elapsed:.2f} seconds.")
        return clean_text(extracted_text)

    except Exception as e:
        logger.error(f"PDF OCR failed: {str(e)}")
        raise

def extract_text(file_path: str) -> str:
    """
    Detect file type and perform OCR.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    return extract_text_from_image(file_path)