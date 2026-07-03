from app.services.pdf_service import extract_text_from_pdf
from app.services.extraction.header_extractor import extract_header

# CHANGE THIS TO YOUR BANK STATEMENT PDF
PDF_PATH = "bank_statement.pdf"

text = extract_text_from_pdf(PDF_PATH)

header = extract_header(text)

for key, value in header.model_dump().items():
    print(f"{key}: {value}")