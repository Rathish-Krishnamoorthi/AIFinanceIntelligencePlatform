from ..utils.invoice_parser import extract_total


def extract_invoice_text(data: bytes, content_type: str) -> str:
    return "" if content_type == "application/pdf" else data[:100000].decode("utf-8", "ignore")


def extract_invoice_total(text: str) -> float:
    return extract_total(text)
