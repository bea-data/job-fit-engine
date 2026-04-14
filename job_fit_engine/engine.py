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
TRACK_A_REJECT_PREFIX = "Reject from Track A"
NEGATION_TOKENS = {"no", "not", "non", "without"}

IGNORE_PHRASES = [
    "equal opportunity",
    "equal opportunities",
    "reasonable accommodation",
    "reasonable accommodations",
    "diversity and inclusion",
    "diversity & inclusion",
    "about us",
    "our values",
    "privacy notice",
    "application procedure",
    "employment process",
]

APPRENTICESHIP_BOILERPLATE_PHRASES = [
    "off-the-job training",
    "off the job training",
    "apprenticeship standard",
    "knowledge skills and behaviours",
    "knowledge, skills and behaviours",
    "training provider",
    "standard reference",
    "functional skills",
    "end point assessment",
    "endpoint assessment",
    "modules covering",
]

EMPLOYER_DUTY_HEADINGS = [
    "what you'll do at work",
    "what you will do at work",
    "what you'll do",
    "what you will do",
    "what you'll be doing",
    "what you will be doing",
    "responsibilities",
    "key responsibilities",
    "main responsibilities",
    "role summary",
    "about the role",
    "job purpose",
    "duties",
    "main duties",
    "day to day",
    "day-to-day",
    "the role",
]

REQUIREMENT_HEADINGS = [
    "entry requirements",
    "requirements",
    "essential requirements",
    "essential criteria",
    "person specification",
    "skills and experience",
    "what we're looking for",
    "what we are looking for",
    "what you need",
    "qualifications",
    "experience required",
]

SUPPORT_HEADINGS = [
    "training provided",
    "training and support",
    "learning and development",
    "support and development",
    "what we offer",
    "development opportunities",
]

BOILERPLATE_HEADINGS = [
    "training to be provided",
    "training course",
    "training course contents",
    "course contents",
    "apprenticeship standard",
    "provider information",
    "your training plan",
]

CANDIDATE_GRADUATION_YEAR = 2022

STUDENT_ONLY_PHRASES = [
    "current students",
    "current student",
    "penultimate year students",
    "penultimate year student",
    "final year students",
    "final year student",
    "currently enrolled students",
    "currently enrolled student",
]

SOFT_GRADUATE_PHRASES = [
    "recent graduate",
    "recent graduates",
    "new graduate",
    "new graduates",
    "graduate programme",
    "graduate program",
    "graduate scheme",
    "entry level graduate role",
]

UK_RIGHT_TO_WORK_PHRASES = [
    "right to work in the uk",
    "right to work in uk",
    "work in the uk without sponsorship",
    "work in uk without sponsorship",
    "ability to work in the uk without sponsorship",
    "ability to work in uk without sponsorship",
]

CLASS_YEAR_PATTERN = re.compile(r"\bclass of\s+(2025|2026)\b")
GRADUATING_YEAR_PATTERN = re.compile(
    r"\bmust be graduating in\s+(2025|2026)(?:\s+or\s+(2025|2026))?\b"
)
RECENT_GRADUATE_WINDOW_PATTERN = re.compile(
    r"\bgraduat(?:ed|e)\s+within\s+the\s+last\s+(12|24)\s+months\b"
)

CONDITIONAL_ELIGIBILITY_TERMS = [
    "experience",
    "qualification",
    "apprenticeship",
    "a level",
    "a-level",
    "degree",
    "diploma",
    "certificate",
    "btec",
    "gcse",
    "equivalent",
]

CONDITIONAL_GATEWAY_INTRODUCERS = [
    "either",
    "one of the following",
    "may qualify through",
    "qualify through",
    "may be eligible through",
]

STAKEHOLDER_GREEN_TERMS = [
    "individual contributor",
    "heads down",
    "independent work",
    "internal team",
    "focus time",
    "small team",
]

STAKEHOLDER_AMBER_TERMS = [
    "cross functional",
    "collaborate",
    "collaborative",
    "partner",
    "work with teams",
    "stakeholder",
    "stakeholders",
    "communicate",
    "communication",
    "influence",
    "liaise",
    "coordinate with third parties",
    "third parties",
    "respond to queries",
    "resolve queries",
    "issue handling",
    "chase issues",
    "follow up issues",
    "buy in",
    "buy-in",
    "dependency management",
]

STAKEHOLDER_RED_TERMS = [
    "stakeholder management",
    "manage stakeholders",
    "stakeholder relationships",
    "relationship management",
    "business partnering",
    "business partner",
    "lead workshops",
    "run workshops",
    "requirements gathering",
    "gather requirements",
    "present to senior stakeholders",
    "present to executives",
    "persuade stakeholders",
    "client facing",
    "customer facing",
]

STAKEHOLDER_BUSINESS_CONTEXT_TERMS = [
    "business analyst",
    "business partner",
    "customer success",
    "account management",
    "project manager",
    "product manager",
    "external clients",
]

HIGH_STAKEHOLDER_OWNERSHIP_TERMS = {
    "stakeholder management",
    "manage stakeholders",
    "stakeholder relationships",
    "relationship management",
    "business partnering",
    "business partner",
    "client facing",
    "customer facing",
}

SECTION_KIND_DUTIES = "duties"
SECTION_KIND_REQUIREMENTS = "requirements"
SECTION_KIND_SUPPORT = "support"
SECTION_KIND_BOILERPLATE = "boilerplate"
SECTION_KIND_OTHER = "other"

ROLE_CORE_SECTION_KINDS = {
    SECTION_KIND_DUTIES,
    SECTION_KIND_REQUIREMENTS,
    SECTION_KIND_OTHER,
}

TECHNICAL_CORE_ALIGNMENT_TERMS = [
    "data engineer",
    "data engineering",
    "engineering team",
    "backend",
    "back end",
    "platform",
    "infrastructure",
    "quality assurance",
    "qa",
    "test automation",
    "software engineer",
    "automation",
    "pipeline",
    "pipelines",
    "etl",
    "api",
    "apis",
    "validation",
    "testing",
    "monitoring",
]

HIGH_CONFIDENCE_TECHNICAL_CORE_TERMS = {
    "data engineer",
    "data engineering",
    "backend",
    "back end",
    "platform",
    "infrastructure",
    "quality assurance",
    "qa",
    "test automation",
    "software engineer",
    "pipeline",
    "pipelines",
    "etl",
}

TECHNICAL_IMPLEMENTATION_TERMS = [
    "build pipelines",
    "build data pipelines",
    "maintain data pipelines",
    "pipeline",
    "pipelines",
    "etl",
    "automation",
    "automate",
    "testing",
    "validation",
    "debugging",
    "troubleshooting",
    "root cause",
    "api",
    "apis",
    "database",
    "python",
    "scripts",
    "monitoring",
    "implementation",
    "implement",
    "data platform",
    "backend",
    "infrastructure",
]

HIGH_CONFIDENCE_IMPLEMENTATION_TERMS = {
    "build pipelines",
    "build data pipelines",
    "maintain data pipelines",
    "pipeline",
    "pipelines",
    "etl",
    "automation",
    "automate",
    "api",
    "apis",
    "data platform",
    "backend",
    "infrastructure",
    "testing",
    "validation",
}

TECHNICAL_TOOL_TERMS = [
    "sql",
    "systems",
    "system",
    "excel",
    "spreadsheet",
    "power bi",
    "vba",
    "reporting tools",
    "data analysis",
]

DOMAIN_OPERATIONS_CORE_TERMS = [
    "analyst",
    "operations",
    "operational",
    "policy",
    "policies",
    "pensions",
    "reconciliation",
    "reconcile",
    "reporting",
    "procedure guide",
    "procedure guides",
    "procedures",
    "records",
    "query",
    "queries",
    "coordinate",
    "coordination",
    "third party",
    "third parties",
    "administration system",
    "scheme",
    "schemes",
    "case",
    "cases",
    "issue",
    "issues",
    "incident",
    "incidents",
    "onboarding",
    "respond to queries",
    "chase",
    "follow up",
    "follow-up",
    "operational teams",
    "process ownership",
    "process owner",
    "procedural",
]

EXPLICIT_SUPPORT_GREEN_TERMS = [
    "training provided",
    "structured support",
    "structured onboarding",
    "onboarding support",
    "structured induction",
    "induction",
    "mentorship",
    "mentor",
    "learn on the job",
    "learning and development",
    "development programme",
    "development program",
    "apprenticeship",
    "shadowing",
    "buddy",
    "coaching",
    "supportive manager",
    "feedback",
    "training and support",
    "day release study",
    "day-release study",
]


def clean_description(text: str) -> str:
    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        lowered = stripped.lower()
        if not stripped:
            continue
        if any(phrase in lowered for phrase in IGNORE_PHRASES):
            continue
        if any(phrase in lowered for phrase in APPRENTICESHIP_BOILERPLATE_PHRASES):
            continue
        cleaned_lines.append(stripped)
    return "\n".join(cleaned_lines).strip()


def build_scoring_text(cleaned_description: str) -> tuple[list["ParsedSection"], str]:
    sections = parse_description_sections(cleaned_description)
    priority_sections = [
        section.text
        for section in sections
        if section.kind in {SECTION_KIND_DUTIES, SECTION_KIND_REQUIREMENTS, SECTION_KIND_SUPPORT}
    ]
    other_sections = [
        section.text for section in sections if section.kind == SECTION_KIND_OTHER
    ]
    fallback_sections = [
        section.text for section in sections if section.kind != SECTION_KIND_BOILERPLATE
    ]

    if priority_sections:
        scoring_parts = priority_sections + other_sections
    else:
        scoring_parts = fallback_sections

    scoring_text = "\n".join(part for part in scoring_parts if part).strip()
    if not scoring_text:
        scoring_text = cleaned_description
    return sections, scoring_text


def parse_description_sections(cleaned_description: str) -> list["ParsedSection"]:
    sections: list[ParsedSection] = []
    current_heading = ""
    current_kind = SECTION_KIND_OTHER
    current_lines: list[str] = []

    def flush_section() -> None:
        if current_heading or current_lines:
            section_text = "\n".join(current_lines).strip()
            if section_text:
                sections.append(
                    ParsedSection(
                        heading=current_heading,
                        kind=current_kind,
                        text=section_text,
                    )
                )

    for raw_line in cleaned_description.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue

        heading_match = extract_section_heading(stripped)
        if heading_match is not None:
            flush_section()
            current_heading, current_kind, first_content = heading_match
            current_lines = [first_content] if first_content else []
            continue

        current_lines.append(stripped)

    flush_section()

    if not sections and cleaned_description.strip():
        return [
            ParsedSection(
                heading="",
                kind=SECTION_KIND_OTHER,
                text=cleaned_description.strip(),
            )
        ]
    return sections


def extract_section_heading(line: str) -> tuple[str, str, str] | None:
    if ":" in line:
        possible_heading, remainder = line.split(":", 1)
        heading_kind = classify_section_heading(possible_heading)
        if heading_kind != SECTION_KIND_OTHER:
            return possible_heading.strip(), heading_kind, remainder.strip()

    heading_kind = classify_section_heading(line)
    if heading_kind != SECTION_KIND_OTHER and len(line.split()) <= 8:
        return line.strip(), heading_kind, ""
    return None


def classify_section_heading(heading: str) -> str:
    normalized_heading = normalize_heading(heading)

    if matches_heading_pattern(normalized_heading, EMPLOYER_DUTY_HEADINGS):
        return SECTION_KIND_DUTIES
    if matches_heading_pattern(normalized_heading, REQUIREMENT_HEADINGS):
        return SECTION_KIND_REQUIREMENTS
    if matches_heading_pattern(normalized_heading, SUPPORT_HEADINGS):
        return SECTION_KIND_SUPPORT
    if matches_heading_pattern(normalized_heading, BOILERPLATE_HEADINGS):
        return SECTION_KIND_BOILERPLATE
    return SECTION_KIND_OTHER


def normalize_heading(value: str) -> str:
    lowered = value.lower().replace("&", " and ")
    lowered = re.sub(r"[^a-z0-9']+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def matches_heading_pattern(normalized_heading: str, patterns: list[str]) -> bool:
    return any(
        normalized_heading == pattern or normalized_heading.startswith(f"{pattern} ")
        for pattern in patterns
    )


def evaluate_eligibility(job_description: str) -> tuple[str, list[str]]:
    cleaned_description = clean_description(job_description)
    return _evaluate_eligibility(cleaned_description)


def _evaluate_eligibility(cleaned_description: str) -> tuple[str, list[str]]:
    sections = parse_description_sections(cleaned_description)
    normalized_text = normalize_text(cleaned_description)
    lowered_text = cleaned_description.lower()
    requirement_text = "\n".join(
        section.text
        for section in sections
        if section.kind == SECTION_KIND_REQUIREMENTS
    ).lower()

    ineligible_reasons: list[str] = []
    possible_reasons: list[str] = []
    conditional_reasons: list[str] = []
    eligible_reasons: list[str] = []

    student_only_matches = find_matches(normalized_text, STUDENT_ONLY_PHRASES)
    if student_only_matches:
        ineligible_reasons.append(
            f"The role explicitly targets current or still-enrolled students ({format_matches(student_only_matches)}), which excludes a {CANDIDATE_GRADUATION_YEAR} graduate."
        )

    if CLASS_YEAR_PATTERN.search(lowered_text):
        ineligible_reasons.append(
            f"The role is limited to the class of 2025 or 2026, which excludes a {CANDIDATE_GRADUATION_YEAR} graduate."
        )

    if GRADUATING_YEAR_PATTERN.search(lowered_text):
        ineligible_reasons.append(
            f"The role requires candidates to be graduating in 2025 or 2026, which excludes a {CANDIDATE_GRADUATION_YEAR} graduate."
        )

    recent_graduate_window = RECENT_GRADUATE_WINDOW_PATTERN.search(lowered_text)
    if recent_graduate_window:
        months = recent_graduate_window.group(1)
        ineligible_reasons.append(
            f"The role requires candidates who graduated within the last {months} months, which excludes a {CANDIDATE_GRADUATION_YEAR} graduate."
        )

    if ineligible_reasons:
        return "Ineligible", unique_items(ineligible_reasons)

    soft_graduate_matches = find_matches(normalized_text, SOFT_GRADUATE_PHRASES)
    if soft_graduate_matches:
        possible_reasons.append(
            f"The wording ({format_matches(soft_graduate_matches)}) often targets graduates more recent than {CANDIDATE_GRADUATION_YEAR}."
        )

    uk_right_to_work_matches = find_matches(normalized_text, UK_RIGHT_TO_WORK_PHRASES)
    if uk_right_to_work_matches:
        eligible_reasons.append(
            "The UK right-to-work requirement is compatible with a UK citizen who does not need sponsorship."
        )

    conditional_gateway_matches = find_conditional_eligibility_matches(
        requirement_text or lowered_text
    )
    if conditional_gateway_matches:
        conditional_reasons.append(
            "The entry requirements are conditional, with multiple qualifying routes through "
            + format_matches(conditional_gateway_matches)
            + "."
        )

    if possible_reasons:
        return "Possibly ineligible", unique_items(possible_reasons)
    if conditional_reasons:
        return "Conditional", unique_items(conditional_reasons + eligible_reasons)
    if eligible_reasons:
        return "Eligible", unique_items(eligible_reasons)

    return (
        "Unclear",
        [
            "The description does not state an eligibility rule that clearly helps or excludes a 2022 UK citizen who does not need sponsorship."
        ],
    )


@dataclass(frozen=True)
class ParsedSection:
    heading: str
    kind: str
    text: str


@dataclass(frozen=True)
class RuleContext:
    original_text: str
    normalized_text: str
    years_required: int | None
    sections: list[ParsedSection]


def evaluate_job_description(job_description: str) -> EvaluationResult:
    """Score a job description against the Track A rubric."""
    cleaned_description = clean_description(job_description)
    eligibility_status, eligibility_reasons = _evaluate_eligibility(cleaned_description)
    sections, scoring_text = build_scoring_text(cleaned_description)
    low_confidence = len(scoring_text.split()) < 40

    context = RuleContext(
        original_text=cleaned_description,
        normalized_text=normalize_text(scoring_text),
        years_required=extract_max_years(scoring_text),
        sections=sections,
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
    stretch_risk, stretch_reason = evaluate_stretch_risk(results)

    total_score = round(sum(result.score for result in results), 1)
    critical_red_flags = [
        result.name
        for result in results
        if result.number in CRITICAL_CATEGORY_NUMBERS and result.band == RED
    ]
    verdict = evaluate_track_a_verdict(
        results,
        total_score=total_score,
        critical_red_flags=critical_red_flags,
        stretch_risk=stretch_risk,
        eligibility_status=eligibility_status,
    )
    if low_confidence:
        verdict = f"{verdict} (low confidence: limited input)"
    track_b_status, track_b_reason = evaluate_track_b(results, verdict)

    return EvaluationResult(
        eligibility_status=eligibility_status,
        eligibility_reasons=eligibility_reasons,
        stretch_risk=stretch_risk,
        stretch_reason=stretch_reason,
        track_b_status=track_b_status,
        track_b_reason=track_b_reason,
        category_results=results,
        total_score=total_score,
        critical_red_flags=critical_red_flags,
        verdict=verdict,
    )


def evaluate_stretch_risk(category_results: list[CategoryResult]) -> tuple[str, str]:
    categories = {result.number: result for result in category_results}

    core_alignment = categories[1]
    technical_fit = categories[2]
    barrier_to_entry = categories[3]
    day_one_usefulness = categories[4]
    stakeholder_load = categories[5]
    ambiguity_level = categories[6]
    structure = categories[7]
    ramp_up_realism = categories[8]
    internal_vs_client = categories[9]
    training_support = categories[12]

    technical_stretch = technical_fit.band in {AMBER, RED} or barrier_to_entry.band in {
        AMBER,
        RED,
    }
    stacked_technical_stretch = technical_fit.band in {AMBER, RED} and barrier_to_entry.band in {
        AMBER,
        RED,
    }

    support_signals = [
        result
        for result in (structure, training_support, stakeholder_load)
        if result.band == GREEN
    ]
    weak_social_load = [
        result
        for result in (stakeholder_load, ambiguity_level, structure, training_support)
        if result.band in {AMBER, RED}
    ]

    if technical_stretch and support_signals:
        return (
            "Supported stretch",
            "Technical stretch is present, but it is buffered by "
            + format_category_bands(support_signals)
            + ".",
        )

    if (
        core_alignment.band == GREEN
        and technical_fit.band in {GREEN, AMBER}
        and barrier_to_entry.band in {GREEN, AMBER}
        and day_one_usefulness.band in {GREEN, AMBER}
        and ramp_up_realism.band == GREEN
        and training_support.band == GREEN
        and stakeholder_load.band != RED
        and internal_vs_client.band != RED
    ):
        return (
            "Supported stretch",
            "The role looks like an early-career technical stretch, but the support and day-one expectations look well scaffolded.",
        )

    if stacked_technical_stretch and weak_social_load:
        return (
            "High-risk stretch",
            "Both technical scope categories are stretched ("
            + format_category_bands([technical_fit, barrier_to_entry])
            + "), and the role also adds "
            + format_category_bands(weak_social_load)
            + ".",
        )

    if technical_stretch:
        return (
            "Moderate stretch",
            "There is some technical stretch ("
            + format_category_bands(
                [
                    result
                    for result in (technical_fit, barrier_to_entry)
                    if result.band in {AMBER, RED}
                ]
            )
            + "), but it does not form the full high-risk pattern.",
        )

    return (
        "Moderate stretch",
        "Technical stretch signals are limited, so this does not look like a high-risk stretch pattern.",
    )


def evaluate_track_a_verdict(
    category_results: list[CategoryResult],
    *,
    total_score: float,
    critical_red_flags: list[str],
    stretch_risk: str,
    eligibility_status: str,
) -> str:
    if critical_red_flags:
        return TRACK_A_REJECT_PREFIX

    categories = {result.number: result for result in category_results}
    barrier_to_entry = categories[3]
    ramp_up_realism = categories[8]

    if total_score >= 80:
        low_gating_friction = (
            eligibility_status in {"Eligible", "Unclear"}
            and barrier_to_entry.band == GREEN
            and ramp_up_realism.band == GREEN
        )
        if low_gating_friction:
            return "Apply immediately"
        if eligibility_status == "Conditional":
            return "Apply if eligibility can be evidenced clearly"
        return "Apply"
    if total_score >= 70:
        return "Apply"
    return TRACK_A_REJECT_PREFIX


def evaluate_track_b(
    category_results: list[CategoryResult],
    verdict: str,
) -> tuple[str | None, str | None]:
    if not is_track_a_reject(verdict):
        return None, None

    categories = {result.number: result for result in category_results}
    safety_categories = [
        categories[5],
        categories[6],
        categories[7],
        categories[10],
        categories[14],
    ]
    unsafe_categories = [result for result in safety_categories if result.band == RED]
    if unsafe_categories:
        return (
            "Not suitable for Track B",
            "Track B is ruled out by red safety signals in "
            + format_category_bands(unsafe_categories)
            + ".",
        )

    support_categories = [
        categories[4],
        categories[8],
        categories[11],
        categories[12],
        categories[15],
    ]
    stable_support_categories = [
        result for result in support_categories if result.band in {GREEN, AMBER}
    ]

    if len(stable_support_categories) >= 4:
        return (
            "Strong Buffer",
            "Track A rejects the role, but it still looks survivable in the short term because "
            + format_category_bands(stable_support_categories)
            + " stay supportive while the core safety categories avoid red.",
        )

    mixed_support_categories = [
        result for result in support_categories if result.band == RED
    ] or support_categories
    return (
        "Weak Buffer",
        "The role avoids Track B disqualifiers, but the support and stability picture is mixed: "
        + format_category_bands(mixed_support_categories)
        + ".",
    )


def is_track_a_reject(verdict: str) -> bool:
    return verdict.startswith(TRACK_A_REJECT_PREFIX)


def find_role_core_matches(context: RuleContext, phrases: Iterable[str]) -> list[str]:
    return find_matches_in_sections(
        context.sections,
        phrases,
        allowed_kinds=ROLE_CORE_SECTION_KINDS,
    )


def has_strong_anchor_match(
    matches: list[str],
    anchor_terms: set[str],
    *,
    minimum_count: int = 2,
) -> bool:
    return any(match in anchor_terms for match in matches) or len(matches) >= minimum_count


def evaluate_core_alignment(context: RuleContext) -> CategoryResult:
    technical_core_matches = find_role_core_matches(
        context, TECHNICAL_CORE_ALIGNMENT_TERMS
    )
    tool_matches = find_role_core_matches(context, TECHNICAL_TOOL_TERMS)
    domain_core_matches = find_role_core_matches(context, DOMAIN_OPERATIONS_CORE_TERMS)
    amber_matches = unique_items(
        find_matches(
            context.normalized_text,
            [
                "operations",
                "support engineer",
                "technical support",
                "application support",
                "process improvement",
                "reporting",
                "analyst",
                "implementation",
            ],
        )
        + domain_core_matches
    )
    red_matches = find_matches(
        context.normalized_text,
        [
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
    strong_technical_core = has_strong_anchor_match(
        technical_core_matches,
        HIGH_CONFIDENCE_TECHNICAL_CORE_TERMS,
    )

    if red_matches and not strong_technical_core:
        return make_result(
            1,
            "Core career-path alignment",
            12,
            RED,
            build_reason(
                RED,
                technical_core_matches,
                amber_matches,
                red_matches,
                "The role core looks too stakeholder-heavy and business-facing.",
            ),
        )

    if domain_core_matches and not strong_technical_core:
        overlap_matches = technical_core_matches or tool_matches
        return make_result(
            1,
            "Core career-path alignment",
            12,
            AMBER,
            "The role has some technical overlap ("
            + format_matches(overlap_matches or amber_matches)
            + "), but the core reads more like "
            + format_matches(domain_core_matches)
            + ".",
        )

    if strong_technical_core and len(domain_core_matches) >= 3:
        return make_result(
            1,
            "Core career-path alignment",
            12,
            AMBER,
            "The role still contains engineering-aligned work ("
            + format_matches(technical_core_matches)
            + "), but it is materially mixed with "
            + format_matches(domain_core_matches)
            + ".",
        )

    if strong_technical_core:
        return make_result(
            1,
            "Core career-path alignment",
            12,
            GREEN,
            build_reason(
                GREEN,
                technical_core_matches,
                amber_matches,
                red_matches,
                "The core career-path alignment looks strong.",
            ),
        )

    if tool_matches:
        return make_result(
            1,
            "Core career-path alignment",
            12,
            AMBER,
            "Technical vocabulary appears ("
            + format_matches(tool_matches)
            + "), but tools alone do not make the role a strong engineering fit.",
        )

    band = choose_band([], amber_matches, red_matches, default=AMBER)
    return make_result(
        1,
        "Core career-path alignment",
        12,
        band,
        build_reason(
            band,
            [],
            amber_matches,
            red_matches,
            "The role core looks adjacent rather than directly aligned.",
        ),
    )


def evaluate_technical_fit(context: RuleContext) -> CategoryResult:
    implementation_matches = find_role_core_matches(
        context, TECHNICAL_IMPLEMENTATION_TERMS
    )
    tool_matches = find_role_core_matches(context, TECHNICAL_TOOL_TERMS)
    domain_core_matches = find_role_core_matches(context, DOMAIN_OPERATIONS_CORE_TERMS)
    amber_matches = unique_items(
        find_matches(
            context.normalized_text,
            [
                "reporting",
                "dashboard",
                "documentation",
                "process",
                "spreadsheet",
                "reconciliation",
                "power bi",
                "vba",
                "excel",
            ],
        )
        + tool_matches
    )
    red_matches = find_matches(
        context.normalized_text,
        [
            "coordination",
            "liaise",
            "translate business",
            "present",
            "workshops",
            "business requirements",
        ],
    )
    strong_implementation = has_strong_anchor_match(
        implementation_matches,
        HIGH_CONFIDENCE_IMPLEMENTATION_TERMS,
    )

    if red_matches and not strong_implementation:
        return make_result(
            2,
            "Technical systems fit",
            8,
            RED,
            build_reason(
                RED,
                implementation_matches,
                amber_matches,
                red_matches,
                "The role looks more like coordination than technical delivery.",
            ),
        )

    if (tool_matches or implementation_matches) and domain_core_matches and not strong_implementation:
        overlap_matches = implementation_matches or tool_matches
        return make_result(
            2,
            "Technical systems fit",
            8,
            AMBER,
            "The role uses technical tools ("
            + format_matches(overlap_matches)
            + "), but the day-to-day delivery looks more like "
            + format_matches(domain_core_matches)
            + " than systems-building work.",
        )

    if strong_implementation and len(domain_core_matches) >= 3:
        return make_result(
            2,
            "Technical systems fit",
            8,
            AMBER,
            "There is real technical overlap ("
            + format_matches(implementation_matches)
            + "), but it sits inside a role core shaped by "
            + format_matches(domain_core_matches)
            + ".",
        )

    if strong_implementation:
        return make_result(
            2,
            "Technical systems fit",
            8,
            GREEN,
            build_reason(
                GREEN,
                implementation_matches,
                amber_matches,
                red_matches,
                "Technical systems fit looks strong.",
            ),
        )

    if tool_matches:
        return make_result(
            2,
            "Technical systems fit",
            8,
            AMBER,
            "Tools like "
            + format_matches(tool_matches)
            + " appear, but tool mentions alone do not show a technical systems role.",
        )

    band = choose_band([], amber_matches, red_matches, default=AMBER)
    return make_result(
        2,
        "Technical systems fit",
        8,
        band,
        build_reason(
            band,
            [],
            amber_matches,
            red_matches,
            "Technical systems fit is partial rather than central.",
        ),
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
    green_matches = find_matches(context.normalized_text, STAKEHOLDER_GREEN_TERMS)
    amber_matches = find_matches(context.normalized_text, STAKEHOLDER_AMBER_TERMS)
    red_matches = find_matches_in_sections(
        context.sections,
        STAKEHOLDER_RED_TERMS,
        allowed_kinds={
            SECTION_KIND_DUTIES,
            SECTION_KIND_REQUIREMENTS,
            SECTION_KIND_OTHER,
        },
    )
    business_context_matches = find_matches_in_sections(
        context.sections,
        STAKEHOLDER_BUSINESS_CONTEXT_TERMS,
        allowed_kinds={
            SECTION_KIND_DUTIES,
            SECTION_KIND_REQUIREMENTS,
            SECTION_KIND_OTHER,
        },
    )
    central_red_matches = find_matches_in_sections(
        context.sections,
        STAKEHOLDER_RED_TERMS,
        allowed_kinds={
            SECTION_KIND_DUTIES,
            SECTION_KIND_REQUIREMENTS,
            SECTION_KIND_OTHER,
        },
    )
    direct_client_matches = [
        match for match in red_matches if match in {"client facing", "customer facing"}
    ]
    ownership_matches = [
        match for match in central_red_matches if match in HIGH_STAKEHOLDER_OWNERSHIP_TERMS
    ]

    if (
        direct_client_matches
        or ownership_matches
        or len(central_red_matches) >= 2
        or (central_red_matches and business_context_matches)
    ):
        return make_result(
            5,
            "Stakeholder load",
            8,
            RED,
            build_reason(
                RED,
                green_matches,
                amber_matches,
                red_matches,
                "Stakeholder-facing work looks central to the role.",
            ),
        )

    if red_matches:
        amber_matches = unique_items(amber_matches + red_matches)
        return make_result(
            5,
            "Stakeholder load",
            8,
            AMBER,
            "Some stakeholder-facing language appears ("
            + format_matches(red_matches)
            + "), but it does not look central enough to outweigh the role's technical delivery focus.",
        )

    band = choose_band(green_matches, amber_matches, [], default=AMBER)
    return make_result(
        5,
        "Stakeholder load",
        8,
        band,
        build_reason(
            band,
            green_matches,
            amber_matches,
            [],
            "Stakeholder exposure looks normal for a collaborative technical role.",
        ),
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
            "ad hoc",
        ],
        red_terms=[
            "fast paced",
            "chaotic",
            "reactive",
            "firefighting",
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
            "escalation",
        ],
        red_terms=[
            "urgent",
            "urgent escalations",
            "escalation management",
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
        EXPLICIT_SUPPORT_GREEN_TERMS,
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


def format_category_bands(results: list[CategoryResult]) -> str:
    return ", ".join(f"{result.name} ({result.band.upper()})" for result in results)


def unique_items(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def find_matches_in_sections(
    sections: list[ParsedSection],
    phrases: Iterable[str],
    *,
    allowed_kinds: set[str],
) -> list[str]:
    matches: list[str] = []
    for section in sections:
        if section.kind not in allowed_kinds:
            continue
        section_matches = find_matches(normalize_text(section.text), phrases)
        for match in section_matches:
            if match not in matches:
                matches.append(match)
    return matches


def find_conditional_eligibility_matches(lowered_text: str) -> list[str]:
    matched_terms = [
        term for term in CONDITIONAL_ELIGIBILITY_TERMS if term in lowered_text
    ]
    explicit_gateway = any(
        introducer in lowered_text
        for introducer in CONDITIONAL_GATEWAY_INTRODUCERS
    )
    route_or_count = len(re.findall(r"\bor\b", lowered_text))
    route_pattern = re.compile(
        r"\b("
        + "|".join(re.escape(term) for term in CONDITIONAL_ELIGIBILITY_TERMS)
        + r")\b[^.:\n;]{0,80}\bor\b[^.:\n;]{0,80}\b("
        + "|".join(re.escape(term) for term in CONDITIONAL_ELIGIBILITY_TERMS)
        + r")\b"
    )
    has_gateway_shape = explicit_gateway or (
        route_or_count >= 2 and route_pattern.search(lowered_text) is not None
    )
    if not has_gateway_shape:
        return []
    if len(unique_items(matched_terms)) >= 2:
        return unique_items(matched_terms)
    return []


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
