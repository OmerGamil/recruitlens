def ocr_pdf_bytes(file_bytes: bytes) -> str:
    """OCR fallback for scanned PDFs using pdf2image + pytesseract."""
    try:
        from pdf2image import convert_from_bytes
        import pytesseract

        images = convert_from_bytes(file_bytes, dpi=200)
        pages_text = []
        for img in images:
            pages_text.append(pytesseract.image_to_string(img))
        return "\n".join(pages_text)
    except ImportError:
        return "[OCR unavailable: install pdf2image and pytesseract]"
    except Exception as e:
        return f"[OCR error: {e}]"
