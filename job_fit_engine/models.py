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
    category_results: list[CategoryResult]
    total_score: float
    critical_red_flags: list[str]
    verdict: str
