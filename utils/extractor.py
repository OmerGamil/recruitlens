import re
from datetime import date

import spacy

SKILLS_TAXONOMY = [
    "Python", "SQL", "Excel", "Machine Learning", "Deep Learning", "TensorFlow",
    "scikit-learn", "Pandas", "NLP", "Power BI", "Tableau", "Java", "JavaScript",
    "React", "Node.js", "AWS", "Azure", "Docker", "Git", "Agile", "Scrum",
    "Communication", "Leadership", "Project Management", "Data Analysis",
    "Statistics", "R", "MATLAB", "Spark", "Hadoop", "Kafka", "MongoDB",
    "PostgreSQL", "REST API", "FastAPI", "Flask", "Django", "Selenium",
    "Pytest", "CI/CD", "Kubernetes", "Linux", "Bash", "TypeScript", "Go",
    "Rust", "C++", "C#", ".NET", "Swift", "Kotlin", "Ruby", "Rails",
    "GraphQL", "Redis", "Elasticsearch", "Airflow", "dbt", "Snowflake",
    "BigQuery", "Redshift", "Power Automate", "Looker", "Metabase",
    "PyTorch", "Keras", "OpenCV", "NLTK", "Hugging Face", "Transformers",
    "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly", "Jupyter",
    "GCP", "Terraform", "Ansible", "Jenkins", "GitHub Actions", "CircleCI",
    "JIRA", "Confluence", "Slack", "Figma", "Photoshop", "SAP", "Salesforce",
    "QuickBooks", "Networking", "Cybersecurity", "Penetration Testing",
    "OWASP", "OAuth", "JWT", "Microservices", "Event-Driven Architecture",
    "System Design", "API Design", "Unit Testing", "Integration Testing",
    "Data Engineering", "ETL", "Data Warehousing", "Business Intelligence",
    "A/B Testing", "Product Management", "UX Research", "SEO", "Marketing Analytics",
]

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
PHONE_RE = re.compile(
    r'(?:\+?\d{1,3}[\s\-.])?(?:\(?\d{2,4}\)?[\s\-.])\d{3,4}[\s\-.]?\d{3,4}'
)
LINKEDIN_RE = re.compile(r'(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9_\-]+/?')

DEGREE_KEYWORDS = [
    "Bachelor", "B.S.", "B.Sc", "B.A.", "B.E.", "B.Tech",
    "Master", "M.S.", "M.Sc", "M.A.", "M.E.", "M.Tech", "MBA",
    "PhD", "Ph.D", "Doctorate", "Diploma", "Certificate",
    "Doctor", "BSc", "MSc",
]

# Compile degree patterns with word boundaries for accurate matching
_DEGREE_PATTERNS = [
    re.compile(r'(?<![A-Za-z])' + re.escape(d) + r'(?![A-Za-z])', re.IGNORECASE)
    for d in DEGREE_KEYWORDS
]


def _has_degree_keyword(text: str) -> bool:
    return any(p.search(text) for p in _DEGREE_PATTERNS)

TITLE_KEYWORDS = [
    "Engineer", "Developer", "Analyst", "Manager", "Director", "Lead",
    "Architect", "Scientist", "Consultant", "Specialist", "Coordinator",
    "Designer", "Administrator", "Executive", "Intern", "Associate",
    "Senior", "Junior", "Principal", "Head", "VP", "CTO", "CEO", "CFO",
]

DATE_RE = re.compile(
    r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
    r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
    r'[\s,]*\d{4}|\d{4}',
    re.IGNORECASE,
)

DATE_RANGE_RE = re.compile(
    r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
    r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
    r'[\s,]*(?:19|20)\d{2}\s*[-–—to]+\s*'
    r'(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
    r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
    r'[\s,]*)?(?:(?:19|20)\d{2}|Present|Current|Now)|'
    r'(?:19|20)\d{2}\s*[-–—to]+\s*(?:(?:19|20)\d{2}|Present|Current|Now)',
    re.IGNORECASE,
)

YEAR_RE = re.compile(r'\b(19|20)\d{2}\b')


def extract_email(text: str) -> str:
    match = EMAIL_RE.search(text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    match = PHONE_RE.search(text)
    return match.group(0).strip() if match else ""


def extract_linkedin(text: str) -> str:
    match = LINKEDIN_RE.search(text)
    return match.group(0) if match else ""


def extract_skills(text: str, taxonomy: list = None) -> list:
    if taxonomy is None:
        taxonomy = SKILLS_TAXONOMY
    text_lower = text.lower()
    found = []
    for skill in taxonomy:
        pattern = re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
        if pattern.search(text_lower):
            found.append(skill)
    return found


def extract_name(text: str, nlp_model) -> str:
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    first_chunk = '\n'.join(lines[:10])
    doc = nlp_model(first_chunk)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Take only the first line of the entity text (spaCy may span newlines)
            name = ent.text.split('\n')[0].strip()
            if name and not EMAIL_RE.search(name) and len(name) < 60:
                return name
    # Fallback: first non-empty line that looks like a name (2–4 words, title case)
    for line in lines[:5]:
        words = line.split()
        if 1 < len(words) <= 4 and all(w[0].isupper() for w in words if w.isalpha()):
            if not any(c.isdigit() for c in line) and '@' not in line and '|' not in line:
                return line
    return ""


def extract_experience(text: str) -> list:
    entries = []
    lines = text.split('\n')
    current = None

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue

        date_match = DATE_RANGE_RE.search(line_stripped)
        if not date_match:
            if current:
                current["description"] += " " + line_stripped
            continue

        if current:
            entries.append(current)

        # Check if the date is on the SAME line as job info (pipe-separated)
        pipes = [p.strip() for p in line_stripped.split('|') if p.strip()]
        if len(pipes) >= 2:
            # Format: "Title | Company | Date Range"  or  "Title | Date Range"
            title = pipes[0]
            company = pipes[1] if len(pipes) >= 3 else ""
            # Exclude pipe parts that are purely email/linkedin/phone
            if EMAIL_RE.search(title) or LINKEDIN_RE.search(title):
                title = ""
            if company and (EMAIL_RE.search(company) or LINKEDIN_RE.search(company)):
                company = ""
        else:
            # Date range is on its own line; look backwards for title and company
            title = ""
            company = ""
            prev_lines = [lines[j].strip() for j in range(max(0, i - 3), i) if lines[j].strip()]
            for pl in reversed(prev_lines):
                if EMAIL_RE.search(pl) or LINKEDIN_RE.search(pl) or DATE_RANGE_RE.search(pl):
                    continue
                if not title and any(t.lower() in pl.lower() for t in TITLE_KEYWORDS):
                    title = pl
                elif not company and len(pl) > 2 and not _has_degree_keyword(pl):
                    company = pl

        current = {
            "title": title,
            "company": company,
            "dates": date_match.group(0),
            "description": "",
        }

    if current:
        entries.append(current)

    # Keep only entries with a non-empty, sensible title
    filtered = [
        e for e in entries
        if e["title"] and not EMAIL_RE.search(e["title"]) and len(e["title"]) < 120
    ]

    # Deduplicate
    seen: set = set()
    unique = []
    for e in filtered:
        key = (e["title"][:40], e["dates"])
        if key not in seen:
            seen.add(key)
            unique.append(e)

    return unique[:8]


def extract_education(text: str) -> list:
    entries = []
    lines = text.split('\n')

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not _has_degree_keyword(line_stripped):
            continue

        year_match = YEAR_RE.search(line_stripped)

        # If the degree line itself is pipe-separated, parse degree + institution from it
        parts = [p.strip() for p in line_stripped.split('|') if p.strip()]
        degree_str = parts[0] if parts else line_stripped
        institution = ""

        if len(parts) >= 2:
            # Second pipe segment is likely the institution
            for p in parts[1:]:
                if not YEAR_RE.fullmatch(p.strip()) and not YEAR_RE.search(p.strip()) or len(p.strip()) > 6:
                    if not DATE_RANGE_RE.search(p) and not EMAIL_RE.search(p):
                        institution = p.strip()
                        break
        else:
            # Look for institution in adjacent lines (±2), skip date-range lines and email lines
            for j in range(max(0, i - 2), min(len(lines), i + 3)):
                candidate = lines[j].strip()
                if not candidate or candidate == line_stripped:
                    continue
                if DATE_RANGE_RE.search(candidate) or EMAIL_RE.search(candidate):
                    continue
                if any(t.lower() in candidate.lower() for t in TITLE_KEYWORDS):
                    continue
                words = candidate.split()
                if len(words) >= 2 and not _has_degree_keyword(candidate):
                    institution = candidate
                    break

        entries.append({
            "degree": degree_str,
            "institution": institution,
            "year": year_match.group(0) if year_match else "",
        })

    # Deduplicate
    seen = set()
    unique = []
    for e in entries:
        key = e["degree"][:40]
        if key not in seen:
            seen.add(key)
            unique.append(e)

    return unique[:5]


def generate_summary(parsed: dict) -> str:
    name = parsed.get("name", "") or "The candidate"
    skills = parsed.get("skills", [])
    experience = parsed.get("experience", [])
    education = parsed.get("education", [])

    top_skills = ", ".join(skills[:5]) if skills else "various technical skills"

    exp_line = ""
    if experience:
        most_recent = experience[0]
        title = most_recent.get("title", "").strip()
        company = most_recent.get("company", "").strip()
        # Guard: skip if title looks like an email or date
        if title and not EMAIL_RE.search(title) and not DATE_RANGE_RE.search(title) and len(title) < 80:
            if company and not EMAIL_RE.search(company) and len(company) < 60:
                exp_line = f" with recent experience as {title} at {company}"
            else:
                exp_line = f" with experience as {title}"

    edu_line = ""
    if education:
        deg = education[0].get("degree", "").strip()
        inst = education[0].get("institution", "").strip()
        if deg and len(deg) < 80:
            if inst and len(inst) < 60:
                edu_line = f", holding {deg} from {inst}"
            else:
                edu_line = f", holding {deg}"

    sentence1 = f"{name} is a professional{exp_line}{edu_line}."
    sentence2 = f"Their key competencies include {top_skills}."
    return f"{sentence1} {sentence2}"


_MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    "january": 1, "february": 2, "march": 3, "april": 4,
    "june": 6, "july": 7, "august": 8, "september": 9,
    "october": 10, "november": 11, "december": 12,
}


def _parse_date_str(s: str):
    s = s.strip().lower()
    if s in ("present", "current", "now"):
        return date.today()
    m = re.match(r'([a-z]+)\s*,?\s*((?:19|20)\d{2})', s)
    if m:
        month = _MONTH_MAP.get(m.group(1)[:3], 1)
        year = int(m.group(2))
        return date(year, month, 1)
    m = re.match(r'((?:19|20)\d{2})', s)
    if m:
        return date(int(m.group(1)), 1, 1)
    return None


_RANGE_SEP_RE = re.compile(r'\s*[-–—]+\s*|\s+to\s+', re.IGNORECASE)


def _parse_date_range(date_str: str):
    parts = _RANGE_SEP_RE.split(date_str, maxsplit=1)
    if len(parts) != 2:
        return None
    start = _parse_date_str(parts[0])
    end = _parse_date_str(parts[1])
    if start and end and start <= end:
        return (start, end)
    return None


def calculate_years_experience(experience_list: list) -> float:
    """Sum non-overlapping date ranges from experience entries, in years."""
    intervals = []
    for exp in experience_list:
        r = _parse_date_range(exp.get("dates", ""))
        if r:
            intervals.append(r)

    if not intervals:
        return 0.0

    intervals.sort(key=lambda x: x[0])
    merged = [list(intervals[0])]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            if end > merged[-1][1]:
                merged[-1][1] = end
        else:
            merged.append([start, end])

    total_days = sum((end - start).days for start, end in merged)
    return round(total_days / 365.25, 1)


def parse_resume(text: str, nlp_model=None) -> dict:
    if nlp_model is None:
        try:
            nlp_model = spacy.load("en_core_web_sm")
        except OSError:
            nlp_model = None

    # Detect section headers so each extractor only sees its own section.
    # Falls back to full text when no headers are found.
    try:
        from utils.section_detector import detect_sections
        sections = detect_sections(text)
    except ImportError:
        sections = {}

    exp_text = sections.get("experience", text)
    edu_text = sections.get("education", text)
    # Skills: prefer dedicated section but also scan full text (skills appear anywhere)
    skills_text = (sections["skills"] + "\n" + text) if "skills" in sections else text

    name = extract_name(text, nlp_model) if nlp_model else ""
    email = extract_email(text)
    phone = extract_phone(text)
    linkedin = extract_linkedin(text)
    skills = extract_skills(skills_text)
    experience = extract_experience(exp_text)
    education = extract_education(edu_text)

    parsed = {
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "skills": skills,
        "experience": experience,
        "education": education,
        "sections_detected": sorted(sections.keys()),
    }
    parsed["summary"] = generate_summary(parsed)
    return parsed
