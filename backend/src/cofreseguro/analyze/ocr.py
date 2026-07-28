"""OCR for image-based SMS screenshots with graceful fallback."""

from __future__ import annotations

import io
import logging

logger = logging.getLogger("cofreseguro.ocr")


def extract_text_from_image(data: bytes, locale: str = "en") -> tuple[str, bool]:
    try:
        import pytesseract
        from PIL import Image, ImageOps
    except ImportError:
        logger.info("OCR dependencies missing; returning unavailable")
        return ("", False)
    try:
        image = Image.open(io.BytesIO(data))
        image = ImageOps.exif_transpose(image)
        image = ImageOps.grayscale(image)
        image = ImageOps.autocontrast(image)
        lang = "por+eng" if locale.startswith("pt") else "eng"
        try:
            text = pytesseract.image_to_string(image, lang=lang)
        except Exception:
            text = pytesseract.image_to_string(image)
        return (text.strip(), True)
    except Exception as exc:  # noqa: BLE001
        logger.warning("OCR failed: %s", exc)
        return ("", False)
