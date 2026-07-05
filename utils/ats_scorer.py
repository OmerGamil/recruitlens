def compute_ats_score(parsed: dict, raw_text: str) -> dict:
    """
    Returns {"total": 0-100, "breakdown": {category: points}}.
    Scoring rubric (100 pts total):
      contact     20  – name + email + phone + linkedin (5 each)
      skills      25  – 2 pts per skill, capped at 25
      experience  25  – 8 pts per entry, capped at 25
      education   15  – 10 pts for any degree, +5 for postgrad
      length      15  – 1 pt per 50 words, capped at 15
    """
    breakdown = {}

    # Contact completeness (20 pts)
    contact_score = (
        (5 if parsed.get("name") else 0)
        + (5 if parsed.get("email") else 0)
        + (5 if parsed.get("phone") else 0)
        + (5 if parsed.get("linkedin") else 0)
    )
    breakdown["contact"] = contact_score

    # Skills (25 pts)
    skills_score = min(25, len(parsed.get("skills", [])) * 2)
    breakdown["skills"] = skills_score

    # Experience depth (25 pts)
    exp_score = min(25, len(parsed.get("experience", [])) * 8)
    breakdown["experience"] = exp_score

    # Education (15 pts)
    edu_score = 0
    if parsed.get("education"):
        edu_score = 10
        deg = parsed["education"][0].get("degree", "").lower()
        if any(x in deg for x in ["master", "m.s", "m.sc", "mba", "m.e", "m.tech", "phd", "ph.d", "doctor"]):
            edu_score = 15
    breakdown["education"] = edu_score

    # Text length / detail (15 pts)
    word_count = len(raw_text.split())
    length_score = min(15, word_count // 50)
    breakdown["length"] = length_score

    total = sum(breakdown.values())
    return {"total": min(100, total), "breakdown": breakdown}
