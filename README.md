# RecruitLens

AI-powered CV/Resume parser for modern HR teams. Upload a resume and instantly extract structured data — contact info, skills, experience, education — with an ATS readiness score, job-description matching, and full parse history.

## Features

| Page | What it does |
|---|---|
| **Parse Resume** | Upload PDF, DOCX, TXT, or RTF; extract all fields + ATS score (0–100); anonymise PII; optional Claude AI fallback |
| **Batch Upload** | Process up to 10 resumes at once; compare in a sortable table with ATS scores highlighted |
| **Demo** | Explore the bundled sample dataset *or* upload the full Kaggle Resume Dataset CSV |
| **JD Match** | Paste a job description; see matched/missing skills and an overall fit percentage |
| **History** | Browse every parsed resume stored in local SQLite; export or delete records |
| **About** | Methodology, accuracy notes, business use cases |

### Key capabilities

- **Multi-format input** — PDF (text layer + OCR fallback for scanned docs), DOCX, TXT, RTF
- **Section-aware extraction** — detects EXPERIENCE / EDUCATION / SKILLS headers so each extractor only sees its own section
- **Accurate experience calc** — merges overlapping date ranges; returns true non-overlapping years
- **ATS Readiness Score** — 0–100 across contact completeness, skill count, experience depth, education level, and text detail
- **JD Match** — 70 % skill overlap + 30 % keyword overlap composite score
- **LLM fallback** — calls `claude-haiku-4-5` when regex/spaCy find nothing (opt-in; needs `ANTHROPIC_API_KEY`)
- **Anonymisation** — one-click PII redaction before export
- **SQLite history** — every parse auto-saved; browsable and exportable from the History page
- **REST API** — FastAPI `POST /parse` endpoint for programmatic access
- **Optional password gate** — set `RECRUITLENS_PASSWORD` to require login

## Tech Stack

- **Streamlit** — UI framework
- **spaCy `en_core_web_sm`** — Named Entity Recognition (name, org, date)
- **PyMuPDF (fitz)** — PDF text extraction
- **python-docx** — DOCX reading
- **Anthropic SDK** — LLM extraction fallback (`claude-haiku-4-5`)
- **FastAPI + Uvicorn** — REST API layer
- **SQLite** — local parse history (no external DB required)
- **Plotly Express** — interactive charts
- **Pandas** — data manipulation

## Setup

### Prerequisites

- Python 3.10+
- pip

### Install

```bash
cd recruitlens
pip install -r requirements.txt
```

The spaCy model wheel is pinned in `requirements.txt`. If it fails, install manually:

```bash
python -m spacy download en_core_web_sm
```

### Run the Streamlit app

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

### Run the REST API

```bash
uvicorn api:app --reload
```

- `GET  /health` — liveness check
- `POST /parse`  — multipart file upload; returns parsed JSON with `years_experience` and `ats_score`

### Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | *(unset)* | Enables LLM extraction fallback via Claude Haiku |
| `RECRUITLENS_PASSWORD` | *(unset)* | Password-protect the app (leave unset for open access) |

### OCR for scanned PDFs (optional)

Install `pdf2image` and `pytesseract` plus the system Tesseract binary, then uncomment the two lines in `requirements.txt`.

## Streamlit Cloud Deployment

1. Push this folder to a GitHub repository
2. Connect at [share.streamlit.io](https://share.streamlit.io); set **Main file path** to `app.py`
3. Add `ANTHROPIC_API_KEY` in the **Secrets** panel if you want LLM fallback

## Dataset Credit

Sample resumes adapted from the [Resume Dataset](https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset) by Gaurav Dutta on Kaggle (CC BY 4.0).  
The Demo page accepts the full Kaggle CSV upload directly (`UpdatedResumeDataSet.csv` or `Resume.csv`).

## Known Limitations

- **Non-standard layouts** — two-column or table-heavy CVs may extract text out of reading order
- **Name extraction** — uncommon formats or names adjacent to email/phone may confuse NER
- **English only** — spaCy model is English-language
- **LLM fallback cost** — each haiku call costs ~$0.001; disable when not needed
- **OCR** — requires optional system dependencies (Tesseract); omitted from default install

## File Structure

```
recruitlens/
├── app.py                     # Streamlit entry point + auth gate
├── api.py                     # FastAPI REST endpoint
├── auth.py                    # Optional password gate helper
├── pages/
│   ├── 1_Demo.py              # Sample + Kaggle dataset demo
│   ├── 2_Parse_Resume.py      # Single resume upload + ATS + anonymise
│   ├── 3_Batch_Upload.py      # Batch comparison table
│   ├── 4_About.py             # Methodology & use cases
│   ├── 5_JD_Match.py          # Job description match
│   └── 6_History.py           # SQLite parse history
├── data/
│   └── sample_resumes.csv
├── utils/
│   ├── extractor.py           # Core extraction + years calc
│   ├── section_detector.py    # Section header detection
│   ├── file_reader.py         # PDF / DOCX / TXT / RTF reading + OCR
│   ├── ocr.py                 # pytesseract OCR fallback
│   ├── ats_scorer.py          # ATS readiness score
│   ├── jd_matcher.py          # JD skills + keyword overlap
│   ├── anonymizer.py          # PII redaction
│   ├── database.py            # SQLite history
│   ├── llm_extractor.py       # Claude Haiku fallback
│   └── parser.py              # spaCy model loader
├── requirements.txt
└── .streamlit/
    └── config.toml
```
