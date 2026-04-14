import streamlit as st
from job_fit_engine.engine import evaluate_job_description

st.markdown("""
<style>
/* Page */
.stApp {
    background-color: #F7F5F2;
    color: #2F3020;
}

/* Main block spacing */
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 900px;
}

/* Headers */
h1, h2, h3 {
    color: #2F3020 !important;
    letter-spacing: -0.02em;
}

/* Labels */
label, .stMarkdown, .stTextInput label, .stTextArea label {
    color: #2F3020 !important;
}

/* Inputs */
.stTextInput input, .stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #2F3020 !important;
    border: 1px solid #CDCBD6 !important;
    border-radius: 12px !important;
}

/* Buttons */
.stButton > button {
    background-color: #D96846 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background-color: #C2573A !important;
}

/* Generic cards */
.result-card {
    background: #FFFFFF;
    border: 1px solid #CDCBD6;
    border-radius: 16px;
    padding: 1.1rem 1.2rem;
    margin: 1rem 0 1.25rem 0;
    box-shadow: 0 1px 2px rgba(47, 48, 32, 0.05);
}

/* Subtle section cards */
.soft-card {
    background: #FBFAF8;
    border: 1px solid #E4E1E8;
    border-radius: 14px;
    padding: 0.9rem 1rem;
    margin: 0.75rem 0 1rem 0;
}

/* Status pills */
.pill {
    display: inline-block;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
}

.pill-green {
    background-color: #E6EBD8;
    color: #596235;
}

.pill-amber {
    background-color: #F6E7D8;
    color: #A5632A;
}

.pill-red {
    background-color: #F8DDDA;
    color: #B14E3A;
}

/* Score highlight */
.score-box {
    background: #FFF7F3;
    border: 1px solid #F0C6B8;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin: 1rem 0;
    font-weight: 700;
    color: #2F3020;
}

/* Category entries */
.category-card {
    background: #FFFFFF;
    border: 1px solid #E4E1E8;
    border-left: 6px solid #CDCBD6;
    border-radius: 14px;
    padding: 0.95rem 1rem;
    margin: 0.8rem 0;
}

.category-green {
    border-left-color: #596235;
}

.category-amber {
    border-left-color: #D39A4A;
}

.category-red {
    border-left-color: #D96846;
}

/* Bullet spacing */
ul {
    margin-top: 0.3rem;
    margin-bottom: 0.3rem;
}

/* Reduce ugly default alert spacing a bit */
[data-testid="stAlert"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

STATUS_TO_MESSAGE = {
    "Eligible": st.success,
    "Possibly ineligible": st.warning,
    "Ineligible": st.error,
    "Unclear": st.info,
}

def pill_class(value: str) -> str:
    lower = value.lower()
    if "eligible" in lower and "possibly" not in lower and "ineligible" not in lower:
        return "pill pill-green"
    if "supported" in lower or "strong buffer" in lower:
        return "pill pill-green"
    if "moderate" in lower or "possibly" in lower or "weak buffer" in lower or "unclear" in lower:
        return "pill pill-amber"
    return "pill pill-red"


def band_class(band: str) -> str:
    band = band.lower()
    if band == "green":
        return "category-card category-green"
    if band == "amber":
        return "category-card category-amber"
    return "category-card category-red"

STRETCH_TO_MESSAGE = {
    "Supported stretch": st.success,
    "Moderate stretch": st.info,
    "High-risk stretch": st.warning,
}

TRACK_B_TO_MESSAGE = {
    "Strong Buffer": st.success,
    "Weak Buffer": st.warning,
    "Not suitable for Track B": st.error,
}


st.title("Job Fit Engine")

job_title = st.text_input("Enter job title")
job_description = st.text_area("Paste job description", height=250)

if st.button("Evaluate"):
    if not job_description.strip():
        st.warning("Please paste a job description.")
    else:
        result = evaluate_job_description(job_description)

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.subheader("Eligibility")
        st.markdown(
            f'<div class="{pill_class(result.eligibility_status)}">{result.eligibility_status}</div>',
            unsafe_allow_html=True,
        )
        for reason in result.eligibility_reasons:
            st.write(f"- {reason}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.subheader("Stretch classification")
        st.markdown(
            f'<div class="{pill_class(result.stretch_risk)}">{result.stretch_risk}</div>',
            unsafe_allow_html=True,
        )
        st.write(result.stretch_reason)
        st.markdown('</div>', unsafe_allow_html=True)

        if result.track_b_status and result.track_b_reason:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.subheader("Track B fallback")
            st.markdown(
                f'<div class="{pill_class(result.track_b_status)}">{result.track_b_status}</div>',
                unsafe_allow_html=True,
            )
            st.write(result.track_b_reason)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="score-box">Total score: {result.total_score}/100</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**Verdict:** {result.verdict}")

        if result.critical_red_flags:
            st.error("Critical red flags: " + ", ".join(result.critical_red_flags))
        else:
            st.info("Critical red flags: none")

        st.subheader("15-category breakdown")

        for category in result.category_results:
            st.markdown(
                f"""
<div class="{band_class(category.band)}">
    <div style="font-weight:700; font-size:1.02rem; color:#2F3020;">
        {category.number:02d}. {category.name}
    </div>
    <div style="margin-top:0.35rem;"><strong>Band:</strong> {category.band.upper()}</div>
    <div><strong>Score:</strong> {category.score}/{category.weight}</div>
    <div><strong>Reason:</strong> {category.reason}</div>
</div>
""",
                unsafe_allow_html=True,
            )
