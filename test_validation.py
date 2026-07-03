from app.services.pdf_service import extract_text_from_pdf
from app.services.extraction.document_parser import split_document
from app.services.extraction.header_extractor import extract_header
from app.services.extraction.transaction_extractor import extract_transactions
from app.services.validation.validation_service import validate_document

PDF_PATH = "bank_statement.pdf"

text = extract_text_from_pdf(PDF_PATH)

sections = split_document(text)

header = extract_header(sections["header"])

transactions = extract_transactions(
    sections["transactions"]
)

print(validate_document(header, transactions))