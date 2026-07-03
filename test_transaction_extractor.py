from app.services.pdf_service import extract_text_from_pdf
from app.services.extraction.document_parser import split_document
from app.services.extraction.transaction_extractor import extract_transactions

PDF_PATH = "bank_statement.pdf"

text = extract_text_from_pdf(PDF_PATH)

sections = split_document(text)

transactions = extract_transactions(
    sections["transactions"]
)

print("=" * 80)
print("TOTAL TRANSACTIONS")
print("=" * 80)

print(len(transactions))

print()

for t in transactions:

    print(t.model_dump())
    print("-" * 80)