from html import escape

import streamlit as st

from job_fit_engine.engine import evaluate_job_description

APP_CSS = """
<style>
:root {
    --green: #0ADD08;
    --amber: #FF991C;
    --red: #FF000D;
    --page: #F7F4EE;
    --page-highlight: #FBF9F4;
    --card: #FFFFFF;
    --text: #24231F;
    --muted: #6F675E;
    --border: #E8E0D4;
    --shadow: rgba(36, 35, 31, 0.06);
}

.stApp {
    background:
        radial-gradient(circle at top right, rgba(255, 153, 28, 0.06), transparent 30%),
        linear-gradient(180deg, var(--page-highlight) 0%, var(--page) 100%);
    color: var(--text);
}

.block-container {
    max-width: 960px;
    padding-top: 2.75rem;
    padding-bottom: 3.5rem;
}

@media (max-width: 640px) {
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.25rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

h1,
h2,
h3 {
    color: var(--text) !important;
    letter-spacing: -0.03em;
}

h1 {
    margin-bottom: 0.35rem;
}

p,
label,
.stMarkdown,
.stTextInput label,
.stTextArea label {
    color: var(--text) !important;
}

.stTextInput input,
.stTextArea textarea {
    background-color: var(--card) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(36, 35, 31, 0.03);
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: rgba(255, 153, 28, 0.75) !important;
    box-shadow: 0 0 0 4px rgba(255, 153, 28, 0.12) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #FF991C 0%, #FFB247 100%) !important;
    color: #2A1F0D !important;
    border: 1px solid #FF991C !important;
    border-radius: 14px !important;
    padding: 0.68rem 1.35rem !important;
    font-weight: 700 !important;
    box-shadow: 0 10px 18px rgba(255, 153, 28, 0.18);
    transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #F38E12 0%, #FFAC38 100%) !important;
    box-shadow: 0 12px 24px rgba(255, 153, 28, 0.22);
    transform: translateY(-1px);
}

.stButton > button:focus {
    box-shadow: 0 0 0 4px rgba(255, 153, 28, 0.14) !important;
}

.result-card,
.score-box,
.category-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    box-shadow: 0 12px 28px rgba(36, 35, 31, 0.05);
}

.result-card {
    margin: 1rem 0 1.25rem;
    padding: 1.15rem 1.2rem;
    border-left: 4px solid var(--border);
}

.result-green {
    border-left-color: #0ADD08;
}

.result-amber {
    border-left-color: #FF991C;
}

.result-red {
    border-left-color: #FF000D;
}

.section-label {
    margin-bottom: 0.65rem;
    font-size: 1.02rem;
    font-weight: 700;
    color: var(--text);
}

.section-copy {
    margin: 0.2rem 0 0;
    color: var(--text);
    line-height: 1.6;
}

.section-list {
    margin: 0.15rem 0 0;
    padding-left: 1.15rem;
}

.section-list li {
    margin: 0.36rem 0;
    color: var(--text);
    line-height: 1.55;
}

.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.36rem 0.78rem;
    border-radius: 999px;
    font-size: 0.86rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    border: 1px solid transparent;
}

.pill::before {
    content: "";
    width: 0.56rem;
    height: 0.56rem;
    border-radius: 999px;
    background: currentColor;
    flex: 0 0 auto;
}

.pill-compact {
    margin-bottom: 0;
    padding: 0.28rem 0.62rem;
    font-size: 0.78rem;
}

.pill-green {
    background: rgba(10, 221, 8, 0.12);
    border-color: #0ADD08;
    color: #087A08;
}

.pill-amber {
    background: rgba(255, 153, 28, 0.14);
    border-color: #FF991C;
    color: #A55B00;
}

.pill-red {
    background: rgba(255, 0, 13, 0.1);
    border-color: #FF000D;
    color: #B1000B;
}

.score-box {
    margin: 1rem 0 1.25rem;
    padding: 1.15rem 1.2rem;
    border-left: 4px solid #FF991C;
    background: linear-gradient(
        180deg,
        rgba(255, 153, 28, 0.08) 0%,
        rgba(255, 153, 28, 0.04) 100%
    );
}

.score-label {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
}

.score-value {
    margin-top: 0.25rem;
    font-size: 1.95rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1.15;
}

.score-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.6rem;
    margin-top: 0.75rem;
}

.score-key {
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--muted);
}

.category-card {
    margin: 0.85rem 0;
    padding: 1rem 1.05rem;
    border-left: 4px solid var(--border);
}

.category-green {
    border-left-color: #0ADD08;
}

.category-amber {
    border-left-color: #FF991C;
}

.category-red {
    border-left-color: #FF000D;
}

.category-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 0.7rem;
}

.category-title {
    color: var(--text);
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.4;
}

.category-body {
    display: grid;
    gap: 0.3rem;
    color: var(--muted);
    line-height: 1.55;
}

.category-body strong {
    color: var(--text);
}
</style>
"""


def format_score(value: float) -> str:
    numeric_value = float(value)
    return str(int(numeric_value)) if numeric_value.is_integer() else f"{numeric_value:.1f}"


def tone_name(value: str) -> str:
    lower = value.lower().strip()
    if lower in {"green", "amber", "red"}:
        return lower
    if lower in {"eligible", "supported stretch", "strong buffer", "apply", "apply immediately"}:
        return "green"
    if lower.startswith("reject from track a"):
        return "red"
    if "ineligible" in lower and "possibly" not in lower:
        return "red"
    if "high-risk" in lower or "not suitable" in lower:
        return "red"
    if "moderate" in lower or "possibly" in lower or "weak buffer" in lower or "unclear" in lower:
        return "amber"
    return "amber"


def pill_class(value: str) -> str:
    return f"pill pill-{tone_name(value)}"


def pill_class_for_tone(tone: str) -> str:
    return f"pill pill-{tone}"


def card_class_for_tone(tone: str) -> str:
    return f"result-card result-{tone}"


def band_class(band: str) -> str:
    return f"category-card category-{tone_name(band)}"


def detail_html(details: list[str] | str) -> str:
    if isinstance(details, str):
        return f'<p class="section-copy">{escape(details)}</p>'
    items = "".join(f"<li>{escape(detail)}</li>" for detail in details)
    return f'<ul class="section-list">{items}</ul>'


def render_status_card(
    title: str,
    status: str,
    details: list[str] | str,
    *,
    tone: str | None = None,
) -> None:
    resolved_tone = tone or tone_name(status)
    st.markdown(
        f"""
<div class="{card_class_for_tone(resolved_tone)}">
    <div class="section-label">{escape(title)}</div>
    <div class="{pill_class_for_tone(resolved_tone)}">{escape(status)}</div>
    {detail_html(details)}
</div>
""",
        unsafe_allow_html=True,
    )


def render_score_summary(total_score: float, verdict: str) -> None:
    st.markdown(
        f"""
<div class="score-box">
    <div class="score-label">Track A score</div>
    <div class="score-value">{escape(format_score(total_score))}/100</div>
    <div class="score-meta">
        <span class="score-key">Verdict</span>
        <span class="{pill_class(verdict)}">{escape(verdict)}</span>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_category_card(category) -> None:
    st.markdown(
        f"""
<div class="{band_class(category.band)}">
    <div class="category-head">
        <div class="category-title">{category.number:02d}. {escape(category.name)}</div>
        <span class="{pill_class(category.band)} pill-compact">{escape(category.band.upper())}</span>
    </div>
    <div class="category-body">
        <div><strong>Score:</strong> {escape(format_score(category.score))}/{category.weight}</div>
        <div><strong>Reason:</strong> {escape(category.reason)}</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


st.markdown(APP_CSS, unsafe_allow_html=True)

st.title("Job Fit Engine")

job_title = st.text_input("Enter job title")
job_description = st.text_area("Paste job description", height=250)

if st.button("Evaluate"):
    if not job_description.strip():
        st.warning("Please paste a job description.")
    else:
        result = evaluate_job_description(job_description)

        if job_title.strip():
            st.caption(f"Reviewing: {job_title.strip()}")

        render_status_card(
            "Eligibility",
            result.eligibility_status,
            result.eligibility_reasons,
        )
        render_status_card(
            "Stretch Classification",
            result.stretch_risk,
            result.stretch_reason,
        )

        render_score_summary(result.total_score, result.verdict)

        if result.track_b_status and result.track_b_reason:
            render_status_card(
                "Track B Fallback",
                result.track_b_status,
                result.track_b_reason,
            )

        if result.critical_red_flags:
            render_status_card(
                "Critical Red Flags",
                "Present",
                result.critical_red_flags,
                tone="red",
            )
        else:
            render_status_card(
                "Critical Red Flags",
                "None",
                "No critical red flags detected.",
                tone="green",
            )

        st.subheader("15-category breakdown")

        for category in result.category_results:
            render_category_card(category)
