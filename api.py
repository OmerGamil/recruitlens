"""
FastAPI REST layer for RecruitLens.

Start with:
    uvicorn api:app --reload

Endpoints:
    POST /parse   — accepts multipart form file, returns parsed JSON
    GET  /health  — liveness check
"""
import io
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from utils.extractor import parse_resume, calculate_years_experience
from utils.ats_scorer import compute_ats_score
from utils.parser import load_nlp

app = FastAPI(title="RecruitLens API", version="2.0")

_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = load_nlp()
    return _nlp


def _read_bytes(filename: str, file_bytes: bytes) -> str:
    name = filename.lower()
    if name.endswith(".pdf"):
        from utils.file_reader import read_pdf
        return read_pdf(file_bytes)
    elif name.endswith(".docx"):
        from utils.file_reader import read_docx
        return read_docx(file_bytes)
    elif name.endswith(".rtf"):
        from utils.file_reader import read_rtf
        return read_rtf(file_bytes)
    else:
        return file_bytes.decode("utf-8", errors="replace")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/parse")
async def parse_endpoint(file: UploadFile = File(...)):
    allowed = {".pdf", ".docx", ".txt", ".rtf"}
    ext = os.path.splitext(file.filename or "")[-1].lower()
    if ext not in allowed:
        raise HTTPException(status_code=415, detail=f"Unsupported file type: {ext}")

    file_bytes = await file.read()
    raw_text = _read_bytes(file.filename, file_bytes)

    if not raw_text or (raw_text.startswith("[") and "error" in raw_text):
        raise HTTPException(status_code=422, detail="Could not extract text from file.")

    nlp = _get_nlp()
    parsed = parse_resume(raw_text, nlp)
    parsed["years_experience"] = calculate_years_experience(parsed["experience"])
    parsed["ats_score"] = compute_ats_score(parsed, raw_text)["total"]

    return JSONResponse(content=parsed)
