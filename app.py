import os
import io
import base64
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List

# Import local modules
from jobs import JOB_DATA
from resume_parser import extract_text
from scorer import calculate_scores
from suggestions import generate_suggestions

# Set page config
st.set_page_config(page_title="AI Resume Screening", layout="wide")

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("AI Resume Screening System")

# ----- Sidebar: Job Role Selection -----
st.sidebar.header("Select Job Role")
job_role = st.sidebar.selectbox("Job Role", list(JOB_DATA.keys()))

# Display job description and required keywords
job_info = JOB_DATA[job_role]
st.sidebar.subheader("Job Description")
st.sidebar.write(job_info["description"])
st.sidebar.subheader("Required Keywords")
st.sidebar.write(", ".join(job_info["keywords"]))

# ----- Main Area: Resume Upload -----
st.header("Upload Resumes")
uploaded_files = st.file_uploader(
    "Upload one or more PDF resumes", type=["pdf"], accept_multiple_files=True
)

if uploaded_files:
    results = []  # List of dicts for each resume
    for uploaded_file in uploaded_files:
        # Read PDF bytes
        file_bytes = uploaded_file.read()
        try:
            resume_text = extract_text(file_bytes)
        except Exception as e:
            st.error(f"Failed to extract text from {uploaded_file.name}: {e}")
            continue

        # Scoring
        scores = calculate_scores(
            resume_text=resume_text,
            job_description=job_info["description"],
            job_keywords=job_info["keywords"]
        )

        # Suggestions
        suggestions = generate_suggestions(scores["missing_keywords"], resume_text)

        result = {
            "Resume Name": uploaded_file.name,
            "Job Role": job_role,
            "Overall Match (%)": scores["overall_match"],
            "ATS Score (%)": scores["ats_score"],
            "Status": scores["status"],
            "Missing Keywords": ", ".join(scores["missing_keywords"]),
            "Suggestions": " | ".join(suggestions),
        }
        results.append(result)

        # ----- Visual Dashboard for this resume -----
        st.subheader(f"Results for {uploaded_file.name}")
        col1, col2 = st.columns([1, 2])
        with col1:
            # Circular gauge for overall match using Plotly
            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=scores["overall_match"],
                    title={"text": "Overall Match"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "#ff7e5f"},
                        "steps": [
                            {"range": [0, 60], "color": "#ff4c4c"},
                            {"range": [60, 80], "color": "#ffbd4c"},
                            {"range": [80, 100], "color": "#4caf50"},
                        ],
                    },
                )
            )
            fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=250)
            st.plotly_chart(fig, use_container_width=True)

            # Status badge
            status = scores["status"]
            if status == "Shortlisted":
                badge = "✅ Shortlisted"
                badge_color = "green"
            elif status == "Consider":
                badge = "🟡 Consider"
                badge_color = "orange"
            else:
                badge = "❌ Not Shortlisted"
                badge_color = "red"
            st.markdown(f"<h3 style='color:{badge_color}'>{badge}</h3>", unsafe_allow_html=True)

        with col2:
            # ATS Score bar
            st.subheader("ATS Compatibility Score")
            st.progress(int(scores["ats_score"]))
            st.caption(f"{scores['ats_score']}% matched keywords")

            # Missing keywords
            if scores["missing_keywords"]:
                with st.expander("Missing Keywords"):
                    st.write(", ".join(scores["missing_keywords"]))
            else:
                st.success("All required keywords present!")

            # Suggestions
            with st.expander("Improvement Suggestions"):
                for s in suggestions:
                    st.markdown(f"- {s}")

    # ----- Aggregate Results Table -----
    if results:
        df = pd.DataFrame(results)
        st.subheader("Summary Table")
        st.dataframe(df[["Resume Name", "Job Role", "Overall Match (%)", "ATS Score (%)", "Status", "Missing Keywords"]])

        # CSV download
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="resume_screening_results.csv",
            mime="text/csv",
        )
else:
    st.info("Upload PDF resumes using the uploader above.")
