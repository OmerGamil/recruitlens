import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from extractor import extract_skills, SKILLS_TAXONOMY


def match_jd(parsed: dict, jd_text: str) -> dict:
    """
    Compare a parsed resume against a job description.
    Returns overlap percentages and lists of matched/missing skills.
    """
    jd_skills = extract_skills(jd_text, SKILLS_TAXONOMY)
    candidate_skills_lower = {s.lower() for s in parsed.get("skills", [])}

    matched = [s for s in jd_skills if s.lower() in candidate_skills_lower]
    missing = [s for s in jd_skills if s.lower() not in candidate_skills_lower]

    skill_match_pct = round(len(matched) / len(jd_skills) * 100, 1) if jd_skills else 0.0

    # Keyword overlap using 4+ character words across JD and resume content
    jd_words = set(re.findall(r'\b[a-z]{4,}\b', jd_text.lower()))
    cv_words = set(re.findall(r'\b[a-z]{4,}\b', parsed.get("summary", "").lower()))
    for exp in parsed.get("experience", []):
        cv_words.update(re.findall(r'\b[a-z]{4,}\b', exp.get("description", "").lower()))
        cv_words.update(re.findall(r'\b[a-z]{4,}\b', exp.get("title", "").lower()))
    for edu in parsed.get("education", []):
        cv_words.update(re.findall(r'\b[a-z]{4,}\b', edu.get("degree", "").lower()))

    overlap = jd_words & cv_words
    keyword_pct = round(len(overlap) / max(len(jd_words), 1) * 100, 1)

    # Composite: 70% skill match + 30% keyword overlap
    overall = round(0.7 * skill_match_pct + 0.3 * keyword_pct, 1)

    return {
        "overall_pct": overall,
        "skill_match_pct": skill_match_pct,
        "keyword_overlap_pct": keyword_pct,
        "matched_skills": matched,
        "missing_skills": missing,
        "jd_skills": jd_skills,
    }
