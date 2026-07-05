import json
import os


def llm_extract_fields(raw_text: str) -> dict:
    """
    Calls claude-haiku-4-5 to extract resume fields when regex/spaCy yield nothing.
    Returns a partial dict with whatever keys Claude could fill in, or {} on error.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {}

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        prompt = (
            "Extract the following fields from the resume text below. "
            "Return ONLY valid JSON — no markdown fences, no explanation — with keys:\n"
            "name (string), email (string), phone (string), linkedin (string), "
            "skills (list of strings), "
            "experience (list of {title, company, dates}), "
            "education (list of {degree, institution, year}).\n\n"
            f"Resume:\n{raw_text[:3000]}\n\nJSON:"
        )

        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        text = message.content[0].text.strip()
        # Strip accidental markdown fences
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n?", "", text)
            text = re.sub(r"\n?```$", "", text)

        return json.loads(text)
    except Exception:
        return {}


import re  # kept at bottom to avoid circular on early return
