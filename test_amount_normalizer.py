from app.services.normalization.amount_normalizer import normalize_amount

amounts = [
    "₹1,234.56",
    "1,234.56",
    "1 234.56",
    "1234.56",
    "500",
    "-500.50",
    "Invalid"
]

for amount in amounts:
    print(f"{amount:15} -> {normalize_amount(amount)}")