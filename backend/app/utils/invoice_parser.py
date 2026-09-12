import re


def extract_total(text: str, default: float = 125000) -> float:
    match = re.search(r"(?:total|amount)[^\d]{0,10}([\d,]+(?:\.\d{2})?)", text, re.I)
    return float(match.group(1).replace(",", "")) if match else default
