import re


def extract_field(text: str, labels: tuple[str, ...], default: str = "") -> str:
    pattern = r"(?:%s)\s*[:#-]?\s*([A-Za-z0-9./_-]+)" % "|".join(labels)
    match = re.search(pattern, text, re.I)
    return match.group(1) if match else default


def extract_total(text: str, default: float = 0) -> float:
    match = re.search(r"(?:total|amount)[^\d]{0,10}([\d,]+(?:\.\d{2})?)", text, re.I)
    return float(match.group(1).replace(",", "")) if match else default
