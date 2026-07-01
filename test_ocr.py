from app.services.ocr_service import extract_text

# Replace this with the path to any image or PDF you want to test
file_path = "sample.pdf"

text = extract_text(file_path)

print("========== OCR OUTPUT ==========")
print(text)