import re

_SECTION_PATTERNS = {
    "experience": re.compile(
        r'^\s*(?:WORK\s+)?(?:EXPERIENCE|EMPLOYMENT|CAREER|PROFESSIONAL\s+(?:HISTORY|EXPERIENCE)|WORK\s+HISTORY)\s*$',
        re.IGNORECASE | re.MULTILINE,
    ),
    "education": re.compile(
        r'^\s*(?:EDUCATION(?:AL\s+BACKGROUND)?|ACADEMIC(?:\s+BACKGROUND)?|QUALIFICATIONS|ACADEMICS)\s*$',
        re.IGNORECASE | re.MULTILINE,
    ),
    "skills": re.compile(
        r'^\s*(?:(?:TECHNICAL\s+|CORE\s+)?SKILLS|CORE\s+COMPETENCIES|EXPERTISE|TECHNOLOGIES|TECH\s+STACK)\s*$',
        re.IGNORECASE | re.MULTILINE,
    ),
    "summary": re.compile(
        r'^\s*(?:SUMMARY|PROFESSIONAL\s+SUMMARY|PROFILE|OBJECTIVE|ABOUT(?:\s+ME)?)\s*$',
        re.IGNORECASE | re.MULTILINE,
    ),
    "certifications": re.compile(
        r'^\s*(?:CERTIFICATIONS?|CERTIFICATES?|LICENSES?\s+(?:&\s+)?(?:AND\s+)?CERTIFICATIONS?|CREDENTIALS)\s*$',
        re.IGNORECASE | re.MULTILINE,
    ),
}


def detect_sections(text: str) -> dict:
    """Return {section_name: body_text} for each section header found in text."""
    matches = []
    for section_name, pattern in _SECTION_PATTERNS.items():
        for m in pattern.finditer(text):
            matches.append((m.start(), m.end(), section_name))

    matches.sort(key=lambda x: x[0])

    sections = {}
    for i, (start, end, name) in enumerate(matches):
        next_start = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        sections[name] = text[end:next_start].strip()

    return sections
