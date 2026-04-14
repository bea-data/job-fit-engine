# Job Fit Engine

`job-fit-engine` is a rule-based Python project that evaluates job descriptions against a structured career-fit rubric.

It turns a qualitative decision into a repeatable, explainable scorecard by checking:

- eligibility
- stretch risk
- role safety and sustainability
- long-term narrative fit

The project includes:

- a Python scoring engine
- a CLI for fast text-file or stdin evaluation
- a Streamlit app for interactive review
- unit tests for representative good-fit, borderline, and reject scenarios

## Why I Built It

Job-search decisions are often subjective, inconsistent, and hard to explain after the fact. I built this project to make that process more structured.

Instead of relying on a vague sense of whether a role "seems right," the engine applies a fixed rubric and returns a transparent breakdown of why a role looks like a fit, a stretch, or a poor match.

## Highlights

- explainable rule-based scoring rather than black-box prediction
- 15 weighted categories covering fit, risk, support, and progression
- explicit eligibility checks tied to candidate constraints
- both CLI and Streamlit interfaces for different workflows
- test coverage for strong-fit, stretch, and reject scenarios

## What It Does

Given a job description, the engine:

1. checks eligibility signals
2. scores the role across 15 weighted categories
3. classifies the role as a supported, moderate, or high-risk stretch
4. flags critical red categories
5. returns a Track A verdict and, when relevant, a Track B fallback assessment

This is intentionally rule-based rather than ML-based. The goal is transparency and consistency, not black-box prediction.

## Tech Stack

- Python
- Streamlit
- `unittest`
- simple package/CLI wiring through `pyproject.toml`

## Scoring Model

The scoring rubric is defined in [specs/track_a_core_bridge.md](specs/track_a_core_bridge.md).

The current implementation evaluates:

- core career-path alignment
- technical systems fit
- barrier to entry
- day-1 usefulness
- stakeholder load
- ambiguity level
- structure and predictability
- ramp-up realism
- internal vs client-facing exposure
- pressure and operational load
- work mode stability
- training and support
- narrative value
- psychological and cultural safety
- stability and progression

Each category is scored as `green`, `amber`, or `red`, then converted into a weighted score out of 100.

Roles that fail Track A can also be routed into a Track B fallback assessment, which helps separate "not ideal, but survivable" from "not suitable."

## Eligibility Assumptions

The eligibility logic is currently tuned to a specific candidate profile:

- 2022 graduate
- UK citizen
- no sponsorship required

That means the engine does more than generic role scoring. It also tries to detect eligibility constraints such as:

- student-only hiring language
- class-year restrictions
- recent-graduate windows
- UK right-to-work requirements

If you want to reuse the engine for a different profile, this is the main area to adapt.

## How It Works

At a high level, the workflow is:

1. clean and normalize the job description
2. detect explicit eligibility signals
3. evaluate 15 rubric categories using phrase and pattern matching
4. calculate a weighted score and critical red flags
5. classify stretch risk and produce a final verdict

The core engine lives in [job_fit_engine/engine.py](job_fit_engine/engine.py), with lightweight data models and separate CLI/UI entry points layered on top.

## Project Structure

- [job_fit_engine/engine.py](job_fit_engine/engine.py): core rule engine and scoring logic
- [job_fit_engine/cli.py](job_fit_engine/cli.py): command-line entry point and formatted report output
- [job_fit_engine/models.py](job_fit_engine/models.py): result models
- [streamlit_app.py](streamlit_app.py): interactive Streamlit UI
- [tests/test_engine.py](tests/test_engine.py): unit coverage for expected scenarios
- [tests/anchors](tests/anchors): example inputs and expected outcomes

## Quick Start

### 1. Install the package

```powershell
python -m pip install -e .
```

If you want to use the Streamlit interface as well:

```powershell
python -m pip install streamlit
```

### 2. Run the CLI

Evaluate inline text:

```powershell
job-fit-engine --text "Junior internal data quality role with structured workflows, training, and no client-facing work."
```

Evaluate a saved file:

```powershell
job-fit-engine --file .\role.txt
```

Evaluate from stdin:

```powershell
Get-Content .\role.txt | job-fit-engine
```

### 3. Run the Streamlit app

```powershell
streamlit run streamlit_app.py
```

Then paste a job description into the app to see:

- eligibility
- stretch classification
- total Track A score
- critical red flags
- per-category reasoning

## Example Outcome

For a structured junior internal data-quality role, the expected result is:

- high overall score, ideally 80+
- `Apply immediately` Track A verdict
- no critical red flags

For a senior client-facing analyst role with high ambiguity, pressure, and minimal onboarding, the expected result is:

- low overall score
- `Reject from Track A`
- multiple red safety or fit signals

See the anchor files in [tests/anchors](tests/anchors) for sample descriptions and expected outcomes.

## Portfolio Value

This project is a good example of:

- translating qualitative judgment into explicit system rules
- designing an evaluation rubric and encoding it in software
- building a small end-to-end tool with both backend logic and usable UI
- writing tests around edge cases and decision consistency

It is less about "predicting the perfect job" and more about building a transparent decision-support system.

## Testing

Run the test suite with:

```powershell
python -m unittest discover -s tests -p "test*.py"
```

The tests cover:

- strong Track A fits
- clear Track A rejects
- eligibility edge cases
- stretch classification behavior
- Track B fallback routing

## Design Principles

This project is designed around a few principles:

- transparent scoring over opaque prediction
- explicit reasoning over single-number output
- safety and survivability, not just keyword matching
- clear career-path fit, not generic job relevance

## Limitations

- The rules are heuristic and intentionally opinionated.
- The engine is tuned to one candidate profile rather than all job seekers.
- It works best with complete job descriptions, not short summaries.
- Streamlit is used by the app but is not currently listed as a package dependency in `pyproject.toml`.

## Future Improvements

- parameterize the candidate profile instead of hard-coding it
- export results as JSON or CSV
- add richer fixtures for real-world job-description formats
- separate rubric configuration from engine code
- package optional UI dependencies more cleanly
