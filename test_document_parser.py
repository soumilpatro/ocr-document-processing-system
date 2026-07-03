from app.services.pdf_service import extract_text_from_pdf
from app.services.extraction.document_parser import split_document

PDF_PATH = "bank_statement.pdf"

text = extract_text_from_pdf(PDF_PATH)

sections = split_document(text)

print("=" * 60)
print("HEADER")
print("=" * 60)
print(sections["header"][:1500])

print("\n")
print("=" * 60)
print("TRANSACTIONS")
print("=" * 60)
print(sections["transactions"])

print("\n")
print("=" * 60)
print("FOOTER")
print("=" * 60)
print(sections["footer"])