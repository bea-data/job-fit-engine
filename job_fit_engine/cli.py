from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .engine import evaluate_job_description
from .models import EvaluationResult


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="job-fit-engine",
        description="Score a job description against the Track A rubric.",
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--text", help="Job description text to score.")
    input_group.add_argument("--file", type=Path, help="Path to a text or markdown file.")
    args = parser.parse_args(argv)

    try:
        job_description = load_job_description(args)
    except ValueError as error:
        parser.error(str(error))

    result = evaluate_job_description(job_description)
    print(format_report(result))
    return 0


def load_job_description(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.file:
        return args.file.read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        stdin_value = sys.stdin.read().strip()
        if stdin_value:
            return stdin_value
    raise ValueError("Provide --text, --file, or pipe a job description on stdin.")


def format_report(result: EvaluationResult) -> str:
    lines = ["Eligibility", f"Status: {result.eligibility_status}"]
    for reason in result.eligibility_reasons:
        lines.append(f"- {reason}")

    lines.extend(
        [
            "",
            "Stretch Risk",
            f"Classification: {result.stretch_risk}",
            f"- {result.stretch_reason}",
        ]
    )
    if result.track_b_status and result.track_b_reason:
        lines.extend(
            [
                "",
                "Track B",
                f"Status: {result.track_b_status}",
                f"- {result.track_b_reason}",
            ]
        )

    lines.extend(["", "Track A Scorecard", ""])
    for category in result.category_results:
        label = f"{category.number:02d}. {category.name}"
        score = f"{format_score(category.score)}/{category.weight}"
        lines.append(
            f"{label:<40} {category.band.upper():<5} {score:>8}  {category.reason}"
        )

    lines.append("")
    lines.append(f"Total score: {format_score(result.total_score)}/100")
    if result.critical_red_flags:
        lines.append("Critical red flags: " + ", ".join(result.critical_red_flags))
    else:
        lines.append("Critical red flags: none")
    lines.append(f"Track A verdict: {result.verdict}")
    return "\n".join(lines)


def format_score(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return f"{value:.1f}"
