from app.services.normalization.text_normalizer import normalize_text

sample = """
ACCOUNT      HOLDER


JOHN      DOE

Account No.     :      1234567890


UPI     AMAZON
"""

print(normalize_text(sample))