import re
import unicodedata


def slugify(
    text: str,
    replacement: str = "-",
    lower: bool = True,
    strict: bool = True,
    trim: bool = True,
) -> str:
    # Unicode normalize to decompose accents
    text = unicodedata.normalize("NFD", text)
    # Remove accents by encoding to ASCII
    text = text.encode("ascii", "ignore").decode("ascii")

    # Remove special characters
    if strict:
        # Keep only word characters and whitespace
        text = re.sub(r"[^\w\s]", "", text)
    else:
        # Keep word characters, whitespace, and hyphens
        text = re.sub(r"[^\w\s-]", "", text)

    # Optionally trim
    if trim:
        text = text.strip()

    # Collapse whitespace into replacement
    text = re.sub(r"\s+", replacement, text)

    # Lowercase if desired
    if lower:
        text = text.lower()

    return text
