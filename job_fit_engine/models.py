from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryResult:
    number: int
    name: str
    weight: int
    band: str
    score: float
    reason: str


@dataclass(frozen=True)
class EvaluationResult:
    eligibility_status: str
    eligibility_reasons: list[str]
    stretch_risk: str
    stretch_reason: str
    track_b_status: str | None
    track_b_reason: str | None
    category_results: list[CategoryResult]
    total_score: float
    critical_red_flags: list[str]
    verdict: str
