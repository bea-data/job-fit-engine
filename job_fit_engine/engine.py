from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from .models import CategoryResult, EvaluationResult

GREEN = "green"
AMBER = "amber"
RED = "red"

BAND_MULTIPLIERS = {
    GREEN: 1.0,
    AMBER: 0.5,
    RED: 0.0,
}

CRITICAL_CATEGORY_NUMBERS = {5, 8, 14}
NEGATION_TOKENS = {"no", "not", "non", "without"}


@dataclass(frozen=True)
class RuleContext:
    original_text: str
    normalized_text: str
    years_required: int | None


def evaluate_job_description(job_description: str) -> EvaluationResult:
    """Score a job description against the Track A rubric."""
    context = RuleContext(
        original_text=job_description,
        normalized_text=normalize_text(job_description),
        years_required=extract_max_years(job_description),
    )

    results = [
        evaluate_core_alignment(context),
        evaluate_technical_fit(context),
        evaluate_barrier_to_entry(context),
        evaluate_day_one_usefulness(context),
        evaluate_stakeholder_load(context),
        evaluate_ambiguity_level(context),
        evaluate_structure(context),
        evaluate_ramp_up_realism(context),
        evaluate_internal_vs_client(context),
        evaluate_pressure(context),
        evaluate_work_mode(context),
    ]

    barrier_band = results[2].band
    ramp_band = results[7].band

    results.extend(
        [
            evaluate_training_support(context, barrier_band=barrier_band, ramp_band=ramp_band),
            evaluate_narrative_value(context),
            evaluate_psychological_safety(context),
            evaluate_stability_progression(context),
        ]
    )

    total_score = round(sum(result.score for result in results), 1)
    critical_red_flags = [
        result.name
        for result in results
        if result.number in CRITICAL_CATEGORY_NUMBERS and result.band == RED
    ]

    if total_score >= 80 and not critical_red_flags:
        verdict = "Apply immediately"
    elif total_score >= 70 and not critical_red_flags:
        verdict = "Apply"
    else:
        verdict = "Reject from Track A"

    return EvaluationResult(
        category_results=results,
        total_score=total_score,
        critical_red_flags=critical_red_flags,
        verdict=verdict,
    )


def evaluate_core_alignment(context: RuleContext) -> CategoryResult:
    return evaluate_keyword_category(
        number=1,
        name="Core career-path alignment",
        weight=12,
        context=context,
        green_terms=[
            "backend",
            "back end",
            "systems",
            "platform",
            "infrastructure",
            "qa",
            "quality assurance",
            "test automation",
            "data quality",
            "validation",
            "software engineer",
            "python",
            "sql",
        ],
        amber_terms=[
            "operations",
            "support engineer",
            "technical support",
            "application support",
            "process improvement",
            "reporting",
            "analyst",
            "implementation",
        ],
        red_terms=[
            "business analyst",
            "stakeholder management",
            "relationship management",
            "client facing",
            "customer success",
            "account management",
            "sales",
            "product manager",
            "project manager",
            "presentations",
        ],
    )


def evaluate_technical_fit(context: RuleContext) -> CategoryResult:
    return evaluate_keyword_category(
        number=2,
        name="Technical systems fit",
        weight=8,
        context=context,
        green_terms=[
            "systems",
            "automation",
            "testing",
            "validate",
            "validation",
            "correctness",
            "debugging",
            "troubleshooting",
            "root cause",
            "api",
            "database",
            "sql",
            "python",
            "scripts",
            "monitoring",
        ],
        amber_terms=[
            "reporting",
            "dashboard",
            "documentation",
            "process",
            "spreadsheet",
        ],
        red_terms=[
            "coordination",
            "liaise",
            "translate business",
            "present",
            "workshops",
            "business requirements",
        ],
    )


def evaluate_barrier_to_entry(context: RuleContext) -> CategoryResult:
    green_terms = [
        "junior",
        "entry level",
        "graduate",
        "assistant",
        "trainee",
        "training provided",
        "no experience required",
    ]
    amber_terms = [
        "desirable",
        "nice to have",
        "exposure to",
        "some experience",
    ]
    red_terms = [
        "senior",
        "lead",
        "principal",
        "manager",
        "architect",
        "expert",
        "proven track record",
    ]

    green_matches = find_matches(context.normalized_text, green_terms)
    amber_matches = find_matches(context.normalized_text, amber_terms)
    red_matches = find_matches(context.normalized_text, red_terms)

    years = context.years_required
    if years is not None:
        if years <= 2:
            return make_result(
                3,
                "Barrier to entry",
                6,
                GREEN,
                f"Experience requirement looks junior-friendly at about {years} year(s).",
            )
        if years <= 4:
            return make_result(
                3,
                "Barrier to entry",
                6,
                AMBER,
                f"Experience requirement is a stretch at about {years} year(s).",
            )
        return make_result(
            3,
            "Barrier to entry",
            6,
            RED,
            f"Experience requirement looks too high at about {years} year(s).",
        )

    band = choose_band(green_matches, amber_matches, red_matches, default=AMBER)
    return make_result(
        3,
        "Barrier to entry",
        6,
        band,
        build_reason(band, green_matches, amber_matches, red_matches, "Experience level is unclear."),
    )


def evaluate_day_one_usefulness(context: RuleContext) -> CategoryResult:
    return evaluate_keyword_category(
        number=4,
        name="Day-1 usefulness",
        weight=6,
        context=context,
        green_terms=[
            "testing",
            "validation",
            "data quality",
            "quality checks",
            "triage",
            "monitoring",
            "support",
            "documentation",
            "bug",
            "defect",
        ],
        amber_terms=[
            "assist",
            "support the team",
            "partner with engineers",
            "learn quickly",
        ],
        red_terms=[
            "own strategy",
            "set roadmap",
            "define architecture",
            "greenfield",
            "build from scratch",
            "thought leadership",
        ],
    )


def evaluate_stakeholder_load(context: RuleContext) -> CategoryResult:
    return evaluate_keyword_category(
        number=5,
        name="Stakeholder load",
        weight=8,
        context=context,
        green_terms=[
            "individual contributor",
            "heads down",
            "independent work",
            "internal team",
            "focus time",
            "small team",
        ],
        amber_terms=[
            "cross functional",
            "collaborate",
            "partner",
            "work with teams",
        ],
        red_terms=[
            "stakeholder management",
            "manage stakeholders",
            "relationship management",
            "client facing",
            "customer facing",
            "workshops",
            "present to",
            "influence",
            "executive",
        ],
    )


def evaluate_ambiguity_level(context: RuleContext) -> CategoryResult:
    return evaluate_keyword_category(
        number=6,
        name="Ambiguity level",
        weight=8,
        context=context,
        green_terms=[
            "clear requirements",
            "acceptance criteria",
            "defined process",
            "standards",
            "procedure",
            "checklist",
            "documented",
        ],
        amber_terms=[
            "adaptable",
            "changing priorities",
            "evolving",
            "flexible",
        ],
        red_terms=[
            "ambiguous",
            "wear many hats",
            "undefined",
            "blank slate",
            "figure it out",
            "unclear",
            "own ambiguous",
        ],
    )


def evaluate_structure(context: RuleContext) -> CategoryResult:
    return evaluate_keyword_category(
        number=7,
        name="Structure / predictability",
        weight=6,
        context=context,
        green_terms=[
            "predictable",
            "structured",
            "routine",
            "repeatable",
            "organised",
            "established process",
            "scheduled",
        ],
        amber_terms=[
            "varied",
            "dynamic",
            "changing",
        ],
        red_terms=[
            "fast paced",
            "chaotic",
            "reactive",
            "firefighting",
            "ad hoc",
            "unstructured",
        ],
    )


def evaluate_ramp_up_realism(context: RuleContext) -> CategoryResult:
    green_matches = find_matches(
        context.normalized_text,
        [
            "training",
            "onboarding",
            "mentorship",
            "shadowing",
            "gradual ramp",
            "learn on the job",
        ],
    )
    amber_matches = find_matches(
        context.normalized_text,
        [
            "self starter",
            "learn quickly",
            "autonomous",
            "comfortable with ambiguity",
        ],
    )
    red_matches = find_matches(
        context.normalized_text,
        [
            "hit the ground running",
            "immediate impact",
            "day one ownership",
            "minimal onboarding",
            "work independently from day one",
            "sink or swim",
            "rapid ramp",
        ],
    )

    years = context.years_required
    if years is not None and years >= 5:
        return make_result(
            8,
            "Ramp-up realism",
            6,
            RED,
            f"The role looks hard to stabilise quickly with a {years}+ year expectation.",
        )

    band = choose_band(green_matches, amber_matches, red_matches, default=AMBER)
    return make_result(
        8,
        "Ramp-up realism",
        6,
        band,
        build_reason(
            band,
            green_matches,
            amber_matches,
            red_matches,
            "Ramp-up expectations are only partly clear.",
        ),
    )


def evaluate_internal_vs_client(context: RuleContext) -> CategoryResult:
    return evaluate_keyword_category(
        number=9,
        name="Internal vs client-facing",
        weight=7,
        context=context,
        green_terms=[
            "internal",
            "internal stakeholders",
            "internal users",
            "back office",
        ],
        amber_terms=[
            "external partners",
            "supplier",
            "vendor",
            "occasional client interaction",
        ],
        red_terms=[
            "client facing",
            "customer facing",
            "customer success",
            "external clients",
            "account management",
        ],
    )


def evaluate_pressure(context: RuleContext) -> CategoryResult:
    return evaluate_keyword_category(
        number=10,
        name="Pressure / operational load",
        weight=7,
        context=context,
        green_terms=[
            "controlled pace",
            "steady",
            "planned work",
            "predictable deadlines",
            "normal hours",
        ],
        amber_terms=[
            "deadlines",
            "service levels",
            "busy periods",
            "time sensitive",
        ],
        red_terms=[
            "urgent",
            "escalation",
            "on call",
            "24 7",
            "incident response",
            "high pressure",
            "time critical",
            "rapid response",
        ],
    )


def evaluate_work_mode(context: RuleContext) -> CategoryResult:
    return evaluate_keyword_category(
        number=11,
        name="Work mode / location stability",
        weight=4,
        context=context,
        green_terms=[
            "remote",
            "hybrid",
            "fixed schedule",
            "standard hours",
            "consistent",
            "one location",
        ],
        amber_terms=[
            "flexible",
            "some travel",
            "onsite as needed",
        ],
        red_terms=[
            "shift work",
            "rotating shifts",
            "weekends",
            "nights",
            "travel required",
            "multiple sites",
            "unpredictable schedule",
        ],
    )


def evaluate_training_support(
    context: RuleContext,
    *,
    barrier_band: str,
    ramp_band: str,
) -> CategoryResult:
    green_matches = find_matches(
        context.normalized_text,
        [
            "training",
            "mentorship",
            "onboarding",
            "supportive manager",
            "feedback",
            "buddy",
            "coaching",
        ],
    )
    amber_matches = find_matches(
        context.normalized_text,
        [
            "collaborative team",
            "support available",
            "some guidance",
        ],
    )
    red_matches = find_matches(
        context.normalized_text,
        [
            "minimal supervision",
            "self starter",
            "independent from day one",
            "no training",
            "hit the ground running",
        ],
    )

    band = choose_band(green_matches, amber_matches, red_matches, default=AMBER)
    if band == RED and barrier_band == GREEN and ramp_band != RED:
        return make_result(
            12,
            "Training / support",
            5,
            AMBER,
            "Support looks light, but the role also looks low-stretch enough to remain plausible.",
        )

    return make_result(
        12,
        "Training / support",
        5,
        band,
        build_reason(
            band,
            green_matches,
            amber_matches,
            red_matches,
            "Support level is unclear from the description.",
        ),
    )


def evaluate_narrative_value(context: RuleContext) -> CategoryResult:
    return evaluate_keyword_category(
        number=13,
        name="Narrative value",
        weight=6,
        context=context,
        green_terms=[
            "platform",
            "engineering",
            "qa",
            "quality",
            "automation",
            "data quality",
            "backend",
            "systems",
        ],
        amber_terms=[
            "operations",
            "technical support",
            "support",
            "analyst",
            "process",
        ],
        red_terms=[
            "customer success",
            "account management",
            "sales",
            "marketing",
            "business development",
            "product manager",
        ],
    )


def evaluate_psychological_safety(context: RuleContext) -> CategoryResult:
    return evaluate_keyword_category(
        number=14,
        name="Psychological / cultural safety",
        weight=6,
        context=context,
        green_terms=[
            "supportive",
            "inclusive",
            "collaborative",
            "respectful",
            "feedback",
            "wellbeing",
            "psychological safety",
        ],
        amber_terms=[
            "resilient",
            "adaptable",
            "paced",
            "growing team",
        ],
        red_terms=[
            "thick skin",
            "competitive",
            "demanding",
            "political",
            "punitive",
            "high pressure culture",
            "challenge culture",
        ],
    )


def evaluate_stability_progression(context: RuleContext) -> CategoryResult:
    return evaluate_keyword_category(
        number=15,
        name="Stability / progression",
        weight=5,
        context=context,
        green_terms=[
            "permanent",
            "career progression",
            "growth",
            "development",
            "progression",
            "promotion",
            "long term",
        ],
        amber_terms=[
            "contract",
            "fixed term",
            "broad exposure",
            "interim",
        ],
        red_terms=[
            "temporary",
            "short term",
            "maternity cover",
            "stop gap",
            "holding pattern",
        ],
    )


def evaluate_keyword_category(
    *,
    number: int,
    name: str,
    weight: int,
    context: RuleContext,
    green_terms: list[str],
    amber_terms: list[str],
    red_terms: list[str],
    default: str = AMBER,
) -> CategoryResult:
    green_matches = find_matches(context.normalized_text, green_terms)
    amber_matches = find_matches(context.normalized_text, amber_terms)
    red_matches = find_matches(context.normalized_text, red_terms)
    band = choose_band(green_matches, amber_matches, red_matches, default=default)
    reason = build_reason(
        band,
        green_matches,
        amber_matches,
        red_matches,
        "The description does not say much here, so this stays in the middle.",
    )
    return make_result(number, name, weight, band, reason)


def choose_band(
    green_matches: list[str],
    amber_matches: list[str],
    red_matches: list[str],
    *,
    default: str,
) -> str:
    if green_matches and not red_matches:
        return GREEN
    if red_matches and not green_matches:
        return RED if len(red_matches) >= len(amber_matches) else AMBER
    if green_matches and red_matches:
        return AMBER
    if amber_matches:
        return AMBER
    if green_matches:
        return GREEN
    if red_matches:
        return RED
    return default


def build_reason(
    band: str,
    green_matches: list[str],
    amber_matches: list[str],
    red_matches: list[str],
    fallback: str,
) -> str:
    if band == GREEN and green_matches:
        return f"Green signals: {format_matches(green_matches)}."
    if band == RED and red_matches:
        return f"Red signals: {format_matches(red_matches)}."

    details = []
    if green_matches:
        details.append(f"green {format_matches(green_matches)}")
    if amber_matches:
        details.append(f"amber {format_matches(amber_matches)}")
    if red_matches:
        details.append(f"red {format_matches(red_matches)}")

    if details:
        return "Mixed signals: " + "; ".join(details) + "."
    return fallback


def make_result(number: int, name: str, weight: int, band: str, reason: str) -> CategoryResult:
    return CategoryResult(
        number=number,
        name=name,
        weight=weight,
        band=band,
        score=weight * BAND_MULTIPLIERS[band],
        reason=reason,
    )


def format_matches(matches: list[str]) -> str:
    return ", ".join(matches[:3])


def find_matches(normalized_text: str, phrases: Iterable[str]) -> list[str]:
    matches: list[str] = []
    for phrase in phrases:
        normalized_phrase = normalize_text(phrase)
        if has_unnegated_match(normalized_text, normalized_phrase) and phrase not in matches:
            matches.append(phrase)
    return matches


def normalize_text(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9+]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return f" {value} "


def has_unnegated_match(normalized_text: str, normalized_phrase: str) -> bool:
    start = normalized_text.find(normalized_phrase)
    while start != -1:
        prefix = normalized_text[max(0, start - 30) : start].strip().split()
        if not prefix or prefix[-1] not in NEGATION_TOKENS:
            return True
        start = normalized_text.find(normalized_phrase, start + 1)
    return False


def extract_max_years(value: str) -> int | None:
    years = []
    for match in re.finditer(
        r"(\d+)\s*(?:\+|plus)?(?:\s*(?:-|to)\s*(\d+))?\s+years?",
        value.lower(),
    ):
        first = int(match.group(1))
        second = int(match.group(2)) if match.group(2) else first
        years.append(max(first, second))

    return max(years) if years else None
