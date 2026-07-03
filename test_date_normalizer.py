from app.services.normalization.date_normalizer import normalize_date

dates = [
    "01/07/2024",
    "1/7/24",
    "01-Jul-2024",
    "01 Jul 2024",
    "2024-07-01",
    "2024/07/01",
    "Invalid Date"
]

for d in dates:
    print(f"{d:20} -> {normalize_date(d)}")