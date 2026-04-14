from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from job_fit_engine.engine import evaluate_eligibility, evaluate_job_description
from job_fit_engine.pdf import extract_text_from_pdf


class FakeUploadedPdf:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload

    def getvalue(self) -> bytes:
        return self.payload


class EngineTests(unittest.TestCase):
    def test_internal_qa_role_passes_track_a(self) -> None:
        description = """
        Junior Data Quality Engineer supporting an internal platform team.
        You will write SQL and Python validation checks, test APIs, investigate
        defects, and monitor data pipelines using clear acceptance criteria and
        documented processes. The role includes structured onboarding, mentorship,
        feedback, and a predictable hybrid schedule with normal hours. This is a
        permanent role with career progression and no client-facing work.
        """

        result = evaluate_job_description(description)

        self.assertEqual(len(result.category_results), 15)
        self.assertGreaterEqual(result.total_score, 80)
        self.assertEqual(result.critical_red_flags, [])
        self.assertEqual(result.verdict, "Apply immediately")
        self.assertIsNone(result.track_b_status)
        self.assertIsNone(result.track_b_reason)

    def test_client_facing_analyst_role_fails_track_a(self) -> None:
        description = """
        Senior Business Analyst working directly with external clients. You will
        manage stakeholders, run workshops, present to executives, own ambiguous
        requirements, and coordinate rapid responses to urgent escalations in a
        fast-paced environment. Candidates should hit the ground running with
        minimal onboarding and bring 5+ years of experience. Travel required.
        """

        result = evaluate_job_description(description)

        self.assertIn("Stakeholder load", result.critical_red_flags)
        self.assertIn("Ramp-up realism", result.critical_red_flags)
        self.assertEqual(result.verdict, "Reject from Track A")

    def test_low_support_can_be_amber_when_role_is_low_stretch(self) -> None:
        description = """
        Junior QA role focused on testing, validation, bug triage, and structured
        checklist-based work for an internal team. Candidates need 1 year of
        experience and should be comfortable working with minimal supervision.
        """

        result = evaluate_job_description(description)
        training_support = next(
            category
            for category in result.category_results
            if category.number == 12
        )

        self.assertEqual(training_support.band, "amber")

    def test_student_only_language_is_ineligible_for_2022_graduate(self) -> None:
        description = """
        Graduate Software Analyst programme for current students and final year
        students only. Applicants must be graduating in 2026.
        """

        status, reasons = evaluate_eligibility(description)

        self.assertEqual(status, "Ineligible")
        self.assertTrue(any("2022 graduate" in reason for reason in reasons))

    def test_graduate_scheme_language_is_possibly_ineligible(self) -> None:
        description = """
        Entry-level graduate role in our software graduate scheme. Recent
        graduates are encouraged to apply.
        """

        status, reasons = evaluate_eligibility(description)

        self.assertEqual(status, "Possibly ineligible")
        self.assertTrue(any("more recent than 2022" in reason for reason in reasons))

    def test_uk_right_to_work_language_is_eligible(self) -> None:
        description = """
        Applicants must already have the right to work in the UK and be able to
        work in the UK without sponsorship.
        """

        status, reasons = evaluate_eligibility(description)

        self.assertEqual(status, "Eligible")
        self.assertTrue(any("right-to-work" in reason.lower() for reason in reasons))

    def test_sponsorship_available_is_neutral(self) -> None:
        description = "Visa sponsorship available for successful candidates."

        status, reasons = evaluate_eligibility(description)

        self.assertEqual(status, "Unclear")
        self.assertEqual(len(reasons), 1)

    def test_track_a_scoring_still_runs_for_ineligible_roles(self) -> None:
        description = """
        Junior Data Quality Engineer for current students and final year students.
        You will write SQL and Python validation checks, test APIs, investigate
        defects, and monitor data pipelines using clear acceptance criteria and
        documented processes. The role includes structured onboarding,
        mentorship, feedback, and a predictable hybrid schedule with normal
        hours. This is a permanent role with career progression and no
        client-facing work.
        """

        result = evaluate_job_description(description)

        self.assertEqual(result.eligibility_status, "Ineligible")
        self.assertTrue(any("2022 graduate" in reason for reason in result.eligibility_reasons))
        self.assertEqual(len(result.category_results), 15)
        self.assertGreater(result.total_score, 0)

    def test_high_risk_stretch_when_technical_and_social_stretch_stack(self) -> None:
        description = """
        Reporting and process analyst role. You will own documentation, reporting,
        and process work, manage stakeholders, run workshops, and handle changing
        priorities with minimal supervision. Candidates should bring 3 years of
        experience.
        """

        result = evaluate_job_description(description)

        self.assertEqual(result.stretch_risk, "High-risk stretch")
        self.assertIn("Both technical scope categories are stretched", result.stretch_reason)

    def test_supported_stretch_when_structure_or_support_buffers_it(self) -> None:
        description = """
        Reporting and process analyst role for an internal team. You will support
        documentation and reporting work in a structured, routine environment with
        established process, training, mentorship, and feedback. Candidates
        should bring 3 years of experience.
        """

        result = evaluate_job_description(description)

        self.assertEqual(result.stretch_risk, "Supported stretch")
        self.assertIn("buffered", result.stretch_reason)

    def test_moderate_stretch_when_only_some_technical_stretch_is_present(self) -> None:
        description = """
        Junior reporting analyst role. You will handle documentation and reporting
        tasks, collaborate across teams, and adapt to changing priorities.
        Candidates should bring 1 year of experience.
        """

        result = evaluate_job_description(description)

        self.assertEqual(result.stretch_risk, "Moderate stretch")
        self.assertIn("some technical stretch", result.stretch_reason)

    def test_track_a_reject_can_be_strong_buffer(self) -> None:
        description = """
        Internal reporting coordinator role handling routine documentation and
        support tasks. Structured onboarding, hybrid working, and permanent
        contract.
        """

        result = evaluate_job_description(description)

        self.assertTrue(result.verdict.startswith("Reject from Track A"))
        self.assertEqual(result.track_b_status, "Strong Buffer")
        self.assertIn("survivable in the short term", result.track_b_reason)

    def test_track_a_reject_can_be_weak_buffer(self) -> None:
        description = """
        Internal reporting coordinator role handling routine documentation and
        support tasks. Routine work, but travel required and temporary contract.
        """

        result = evaluate_job_description(description)

        self.assertTrue(result.verdict.startswith("Reject from Track A"))
        self.assertEqual(result.track_b_status, "Weak Buffer")
        self.assertIn("mixed", result.track_b_reason)

    def test_track_a_reject_can_be_not_suitable_for_track_b(self) -> None:
        description = """
        Internal reporting coordinator role with routine documentation work, but
        candidates must manage stakeholders and urgent escalations in a
        fast-paced environment. Hybrid working and permanent contract.
        """

        result = evaluate_job_description(description)

        self.assertTrue(result.verdict.startswith("Reject from Track A"))
        self.assertEqual(result.track_b_status, "Not suitable for Track B")
        self.assertIn("red safety signals", result.track_b_reason)


class PdfExtractionTests(unittest.TestCase):
    @patch("job_fit_engine.pdf.PdfReader")
    def test_extract_text_from_pdf_joins_text_from_all_pages(self, mock_pdf_reader) -> None:
        first_page = Mock()
        first_page.extract_text.return_value = "First page"
        second_page = Mock()
        second_page.extract_text.return_value = "Second page"
        third_page = Mock()
        third_page.extract_text.return_value = None
        mock_pdf_reader.return_value.pages = [first_page, second_page, third_page]

        extracted_text = extract_text_from_pdf(FakeUploadedPdf(b"%PDF-test"))

        self.assertEqual(extracted_text, "First page\nSecond page")

    def test_extract_text_from_pdf_raises_clear_error_when_pypdf_is_missing(self) -> None:
        with patch("job_fit_engine.pdf.PdfReader", None):
            with self.assertRaisesRegex(RuntimeError, "pypdf"):
                extract_text_from_pdf(FakeUploadedPdf(b"%PDF-test"))


if __name__ == "__main__":
    unittest.main()
