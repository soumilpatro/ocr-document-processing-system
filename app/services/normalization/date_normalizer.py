from datetime import datetime


SUPPORTED_DATE_FORMATS = [
    "%d/%m/%Y",
    "%d/%m/%y",
    "%d-%m-%Y",
    "%d-%m-%y",
    "%d.%m.%Y",
    "%d.%m.%y",
    "%d %b %Y",
    "%d %b %y",
    "%d %B %Y",
    "%d %B %y",
    "%d-%b-%Y",
    "%d-%b-%y",
    "%Y-%m-%d",
    "%Y/%m/%d",
]


def normalize_date(date_string: str) -> str | None:
    """
    Convert multiple bank statement date formats
    into ISO format (YYYY-MM-DD).
    """

    if not date_string:
        return None

    date_string = date_string.strip()

    for fmt in SUPPORTED_DATE_FORMATS:
        try:
            parsed = datetime.strptime(date_string, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None