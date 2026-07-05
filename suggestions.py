from typing import List


def generate_suggestions(missing_keywords: List[str], resume_text: str) -> List[str]:
    """Generate simple improvement suggestions based on missing keywords.

    The function returns a list of human‑readable suggestions. It looks at the
    missing keywords and adds generic advice for formatting, ATS optimisation,
    and skill enrichment.
    """
    suggestions = []
    if missing_keywords:
        suggestions.append(
            f"Add the following relevant keywords to your resume: {', '.join(missing_keywords)}."
        )
        suggestions.append(
            "Highlight measurable achievements (e.g., increased sales by 15%) to strengthen impact."
        )
    else:
        suggestions.append("Your resume already contains all the key terms for this role.")

    # Generic formatting and ATS tips
    suggestions.extend([
        "Use a clean, ATS‑friendly layout: simple headings, standard fonts, and no tables or images.",
        "Include a concise summary at the top that mentions the target role and top skills.",
        "Tailor each bullet point to demonstrate how you used the required skills in past roles.",
        "Proofread for spelling and grammar errors; ATS may penalise typo‑laden resumes.",
        "Save the final resume as a PDF with searchable text (not scanned images)."
    ])
    return suggestions
