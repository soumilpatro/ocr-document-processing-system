import re


def normalize_text(text: str) -> str:
    """
    Normalize OCR text while preserving document structure.
    """

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove extra spaces within lines
    normalized_lines = []

    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()
        normalized_lines.append(line)

    # Remove excessive blank lines
    cleaned_lines = []
    previous_blank = False

    for line in normalized_lines:
        if line == "":
            if not previous_blank:
                cleaned_lines.append("")
            previous_blank = True
        else:
            cleaned_lines.append(line)
            previous_blank = False

    return "\n".join(cleaned_lines).strip()