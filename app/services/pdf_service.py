from pypdf import PdfReader

from app.services.ocr_service import (
    extract_text_from_pdf as extract_text_using_ocr
)


def extract_text_from_digital_pdf(pdf_path: str) -> str:
    """
    Extract embedded text from a digital PDF using pypdf.
    """

    reader = PdfReader(pdf_path)

    extracted_text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_text += page_text + "\n"

    return extracted_text.strip()


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Try extracting embedded text first.
    If unsuccessful, fall back to OCR.
    """

    text = extract_text_from_digital_pdf(pdf_path)

    # If enough text exists, use it.
    if len(text.strip()) > 50:
        return text

    # Otherwise run OCR.
    return extract_text_using_ocr(pdf_path)