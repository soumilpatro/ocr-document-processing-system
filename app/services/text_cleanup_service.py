import re


def normalize_spaces(text: str) -> str:
    """
    Replace multiple spaces and tabs with a single space.
    """
    return re.sub(r"[ \t]+", " ", text)


def normalize_newlines(text: str) -> str:
    """
    Replace multiple blank lines with a single newline.
    """
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text


def correct_common_ocr_errors(text: str) -> str:
    """
    Correct common OCR mistakes.
    """

    corrections = {
        "|": "I",
        "§": "S",
        "ﬁ": "fi",
        "ﬂ": "fl",
    }

    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)

    return text


def clean_text(text: str) -> str:
    """
    Apply all OCR cleanup steps.
    """

    text = normalize_spaces(text)

    text = normalize_newlines(text)

    text = correct_common_ocr_errors(text)

    return text.strip()