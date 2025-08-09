"""OCR stub for image-based SMS screenshots."""

from __future__ import annotations


def extract_text_from_image(data: bytes) -> tuple[str, bool]:
    try:
        import io

        import pytesseract
        from PIL import Image
    except ImportError:
        return ("", False)
    try:
        image = Image.open(io.BytesIO(data))
        text = pytesseract.image_to_string(image)
        return (text.strip(), True)
    except Exception:
        return ("", False)
