import streamlit as st
from job_fit_engine.engine import evaluate_job_description


STATUS_TO_MESSAGE = {
    "Eligible": st.success,
    "Possibly ineligible": st.warning,
    "Ineligible": st.error,
    "Unclear": st.info,
}

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

        st.subheader("Eligibility")
        STATUS_TO_MESSAGE[result.eligibility_status](
            f"Status: {result.eligibility_status}"
        )
        for reason in result.eligibility_reasons:
            st.write(f"- {reason}")

        st.subheader("Stretch classification")
        STRETCH_TO_MESSAGE[result.stretch_risk](
            f"Classification: {result.stretch_risk}"
        )
        st.write(result.stretch_reason)

        if result.track_b_status and result.track_b_reason:
            st.subheader("Track B fallback")
            TRACK_B_TO_MESSAGE[result.track_b_status](
                f"Status: {result.track_b_status}"
            )
            st.write(result.track_b_reason)

        st.success(f"Total score: {result.total_score}/100")
        st.write(f"**Verdict:** {result.verdict}")

        if result.critical_red_flags:
            st.error("Critical red flags: " + ", ".join(result.critical_red_flags))
        else:
            st.info("Critical red flags: none")

        st.subheader("15-category breakdown")

        for category in result.category_results:
            st.markdown(
                f"""
**{category.number:02d}. {category.name}**
- Band: **{category.band.upper()}**
- Score: **{category.score}/{category.weight}**
- Reason: {category.reason}
"""
            )
