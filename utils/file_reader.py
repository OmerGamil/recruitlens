import io

_OCR_THRESHOLD = 50  # chars — if PyMuPDF extracts fewer, attempt OCR


def read_pdf(file_bytes: bytes) -> str:
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text_parts = [page.get_text() for page in doc]
        doc.close()
        text = "\n".join(text_parts)
    except Exception as e:
        return f"[PDF read error: {e}]"

    if len(text.strip()) < _OCR_THRESHOLD:
        from utils.ocr import ocr_pdf_bytes
        ocr_text = ocr_pdf_bytes(file_bytes)
        if not ocr_text.startswith("["):
            return ocr_text

    return text


def read_docx(file_bytes: bytes) -> str:
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        return f"[DOCX read error: {e}]"


def read_rtf(file_bytes: bytes) -> str:
    """Best-effort RTF → plain text by stripping RTF control words."""
    import re

    try:
        text = file_bytes.decode("utf-8", errors="replace")
    except Exception:
        return ""

    text = re.sub(r'\\[a-z]+\-?\d*[ ]?', ' ', text)
    text = re.sub(r'[{}]', '', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def read_file(uploaded_file) -> str:
    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        return read_pdf(file_bytes)
    elif name.endswith(".docx"):
        return read_docx(file_bytes)
    elif name.endswith(".rtf"):
        return read_rtf(file_bytes)
    else:
        # .txt and any other plain-text format
        try:
            return file_bytes.decode("utf-8", errors="replace")
        except Exception:
            return ""
