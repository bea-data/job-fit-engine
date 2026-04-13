from __future__ import annotations

import unittest

from job_fit_engine.engine import evaluate_job_description


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


if __name__ == "__main__":
    unittest.main()
