import copy


def anonymize(parsed: dict) -> dict:
    """Return a deep copy of parsed dict with PII fields replaced by placeholders."""
    anon = copy.deepcopy(parsed)

    name = parsed.get("name", "")
    anon["name"] = "[CANDIDATE]" if name else ""
    anon["email"] = "[EMAIL REDACTED]" if parsed.get("email") else ""
    anon["phone"] = "[PHONE REDACTED]" if parsed.get("phone") else ""
    anon["linkedin"] = "[LINKEDIN REDACTED]" if parsed.get("linkedin") else ""

    if name and anon.get("summary"):
        anon["summary"] = anon["summary"].replace(name, "[CANDIDATE]")

    return anon
