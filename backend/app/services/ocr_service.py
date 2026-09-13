from ..utils.invoice_parser import extract_total


def extract_invoice_text(data: bytes, content_type: str) -> str:
    if content_type == "application/pdf":
        import fitz
        document = fitz.open(stream=data, filetype="pdf")
        text = "\n".join(page.get_text() for page in document).strip()
        if text:
            return text[:100000]
        try:
            import pytesseract
            from PIL import Image
            pages = []
            for page in document:
                pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                pages.append(pytesseract.image_to_string(Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)))
            return "\n".join(pages)[:100000]
        except (ImportError, RuntimeError, OSError):
            return ""
    return data[:100000].decode("utf-8", "ignore")


def extract_invoice_total(text: str) -> float:
    return extract_total(text)
