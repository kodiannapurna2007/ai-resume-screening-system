import re
from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _clean_text(text: str) -> str:
    """Basic text cleaning: lower‑case, remove non‑alphanumeric characters."""
    text = text.lower()
    # keep alphanumeric and spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text


def calculate_scores(resume_text: str, job_description: str, job_keywords: List[str]) -> Dict:
    """Calculate similarity and keyword based scores.

    Returns a dictionary with:
        - overall_match: 0‑100 (cosine similarity)
        - ats_score: 0‑100 (keyword match percentage)
        - missing_keywords: list of keywords not found in resume
        - status: one of "Shortlisted", "Consider", "Not Shortlisted"
    """
    # Clean texts
    resume_clean = _clean_text(resume_text)
    job_clean = _clean_text(job_description)

    # TF‑IDF similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_clean, job_clean])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    overall_match = round(similarity * 100, 2)

    # Keyword matching (case‑insensitive)
    resume_words = set(resume_clean.split())
    matched = [kw for kw in job_keywords if kw.lower() in resume_words]
    ats_score = round(len(matched) / len(job_keywords) * 100, 2) if job_keywords else 0.0
    missing_keywords = [kw for kw in job_keywords if kw.lower() not in resume_words]

    # Determine status based on overall_match (as primary metric)
    if overall_match >= 80:
        status = "Shortlisted"
    elif overall_match >= 60:
        status = "Consider"
    else:
        status = "Not Shortlisted"

    return {
        "overall_match": overall_match,
        "ats_score": ats_score,
        "missing_keywords": missing_keywords,
        "status": status,
    }
