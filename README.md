# AI Resume Screening System

## Overview

A modern, dark‑themed web application built with **Streamlit** that lets recruiters or hiring managers:
- Select a job role from a predefined list.
- View the job description and required keywords.
- Upload one or more PDF resumes.
- Automatically extract text from the PDFs (using **PyPDF2**).
- Compare each resume against the job description using **TF‑IDF + cosine similarity** and **keyword matching**.
- See a visual dashboard with circular gauge, progress bars, status badges, missing keywords, and improvement suggestions.
- Download a CSV summary of all results.

The UI follows a premium black‑background, white‑text design with smooth hover animations, rounded buttons, and responsive cards.

## Project Structure

```
ai_resume_screening/
├─ app.py               # Streamlit entry point
├─ jobs.py              # Pre‑defined job descriptions & keywords
├─ resume_parser.py     # PDF text extraction (PyPDF2)
├─ scorer.py            # Scoring logic (TF‑IDF, cosine similarity, keyword match)
├─ suggestions.py       # Generate improvement suggestions
├─ style.css            # Custom dark‑theme CSS
├─ requirements.txt     # Python dependencies
├─ uploads/             # Temporary storage for uploaded PDFs (git‑ignore)
└─ results/             # Generated CSV files (git‑ignore)
```

## Installation

1. **Clone / create the project folder** (if not already created).
2. Open a terminal in the `ai_resume_screening` directory.
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   This will install:
   - streamlit
   - pandas
   - scikit-learn
   - spacy (and the `en_core_web_sm` model is listed as a dependency)
   - PyPDF2
   - plotly
   - numpy
4. (Optional) Verify the spaCy model is available:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running the Application

```bash
streamlit run app.py
```

The app will open in your default browser. Use the sidebar to pick a job role, then upload PDF resumes via the uploader.

## Usage Guide

- **Job Role Selection** – Choose a role; the description and keywords appear in the sidebar.
- **Resume Upload** – Drag‑and‑drop one or multiple PDF files.
- **Results** – For each resume you’ll see:
  - A circular gauge showing the overall similarity score.
  - A progress bar for the ATS keyword match.
  - A status badge (✅ Shortlisted, 🟡 Consider, ❌ Not Shortlisted).
  - Expanders listing missing keywords and tailored improvement suggestions.
- **Summary Table** – After processing all uploads, a table summarises the scores.
- **Download CSV** – Click the button to download `resume_screening_results.csv`.

## Customising Job Roles

Edit `jobs.py` – add or modify entries in the `JOB_DATA` dictionary. Each role requires a `description` (string) and `keywords` (list of strings).

## Extending Functionality

- Swap **PyPDF2** for **pdfplumber** by updating `resume_parser.py`.
- Use a larger spaCy model (`en_core_web_md`) for richer linguistic features.
- Add unit tests for each module.

## License

This project is provided under the MIT License.
