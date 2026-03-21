---
name: fast-multi-agent-tdd
description: Use when the user wants a feature or bug fix delivered under strict Red-Green-Refactor, with a dedicated monitor agent and per-phase audits via $review-with-multi-debate.
---

# Fast Multi Agent TDD

## Overview

Use this skill for real implementation work when the user wants strict TDD and strong phase discipline. Keep implementation ownership with one main agent and use the monitor only for enforcement and audit handoff.

This skill is not for generic reviews, one-line edits, or vague brainstorming. Use it when the task is "build or fix behavior under TDD" and the user cares about phase discipline, regression safety, and auditability.

## Trigger Conditions

Use this skill when the request includes some combination of:

- add a feature or fix a bug
- strict TDD, red-green-refactor, or regression checks
- explicit auditing of each phase
- concern that green or refactor work might quietly mutate tests

Do not use this skill when:

- the user only wants a code review
- the task is pure documentation with no behavior change

## Core Rules

- Red owns test changes. Green and refactor do not edit tests. If a new test is needed later, go back to red.
- Update docs relevant to the code change only after red, green, regression, and refactor are complete. Do not mix README or other doc edits into refactor.
- The main agent owns the critical path and the implementation work.
- A dedicated monitor agent never edits files. It checks phase scope, records violations, and blocks phase completion if boundaries were crossed.
- Do not spawn parallel workers for implementation, exploration, or test drafting. Extra workers here create chaos rather than speed.
- Every phase ends with an audit using `$review-with-multi-debate`.
- After any code change, run the full available test suite. This is the regression check.

## Roles

Keep the setup minimal.

- Main agent: owns the current phase outcome and all file edits for that phase.
- Monitor agent: no file edits, no implementation suggestions, only scope enforcement and audit orchestration.

## Workflow

### 1. Request Map

Before writing tests or code:

- read the nearest guidance files such as `AGENTS.md`, `CLAUDE.md`, `README.md`, and nearby docs
- split the request into concrete requirements
- identify the smallest user-visible slice worth implementing first
- identify the highest-risk execution boundary
- identify the concrete minimal execution path that actually traverses the highest-risk execution boundary
- identify the observable evidence that will prove the boundary was crossed during the test
- decide the likely test level: feature, integration, or unit
- if you plan to rely on lower-level tests because no high-risk integration boundary is actually crossed, justify that with a `strace` or `dtruss` check on the minimal execution path rather than with narrative alone
- derive a short `feature_name` for audit files

Start the monitor agent here. It should open [references/phase_contracts.md](references/phase_contracts.md) and enforce it for the rest of the run.

Audit this phase with `$review-with-multi-debate` using the request-map claim in [references/phase_audits.md](references/phase_audits.md).

### 2. Red

Main goal: produce the next failing test and nothing else.

Allowed actions:

- create or edit tests
- add a brief Gherkin feature file when the behavior is broad enough to need one
- adjust test fixtures only if required by the new test
- write the first failing test at the highest-risk execution boundary identified in Request Map
- if the boundary involves multiple components, process execution, shell, filesystem, network, concurrency, or external tool invocation, an integration test is mandatory
- when an integration test is mandatory, the failing test must assert at least one observable outcome that proves the risky boundary was actually traversed
- command construction or mocked boundary tests do not satisfy this requirement unless the boundary itself is purely local logic
- run the targeted test to confirm the failure reason is missing behavior rather than syntax or setup

Before closing red:

- run the monitor scope check for `red`
- run `$review-with-multi-debate` with the red claim from [references/phase_audits.md](references/phase_audits.md)

### 3. Green

Main goal: make the red test pass with the smallest production change.

Allowed actions:

- edit production code
- add the smallest missing wiring required for the failing test
- run the targeted test until it passes

Forbidden actions:

- editing tests
- broad cleanup
- hidden fallback logic

Before closing green:

- run the monitor scope check for `green`
- run `$review-with-multi-debate` with the green claim from [references/phase_audits.md](references/phase_audits.md)

### 4. Regression Check

Run the full available test suite after the green change. This is not optional.

If the suite is large, you may first run the closest package or component suite, but phase completion still requires the full available suite unless the environment makes that impossible.

Audit this phase with the regression claim in [references/phase_audits.md](references/phase_audits.md).

### 5. Refactor

Only start refactor after green plus regression are both clean.

Allowed actions:

- simplify production code
- remove duplication
- improve naming or structure
- tighten obvious implementation seams

Forbidden actions:

- editing tests
- editing docs such as `README.md`
- sneaking in new behavior
- using refactor as a second green phase

After each refactor change:

- run the full available test suite again
- run the monitor scope check for `refactor`
- audit the phase with the refactor claim from [references/phase_audits.md](references/phase_audits.md)

### 6. Documentation Follow-Up

Only start this step after red, green, regression, and refactor are done.

Allowed actions:

- update docs relevant to the completed code change
- keep doc edits narrow and implementation-aligned

Forbidden actions:

- editing tests
- editing production code
- using docs as a place to sneak in design changes that the code does not implement

Before closing documentation:

- run the monitor scope check for `docs`
- audit the phase with the docs claim from [references/phase_audits.md](references/phase_audits.md)

### 7. Final Closeout

Before finishing:

- confirm each mapped requirement has a passing test
- summarize any unresolved risks
- keep the final explanation short and oversight-friendly

Run the final coverage audit from [references/phase_audits.md](references/phase_audits.md).

## Monitor Protocol

The monitor agent is separate on purpose. Its job is to stop phase bleed.

At each phase boundary:

1. Collect the changed file list for the phase.
2. Run:

```bash
python scripts/phase_guard.py --phase red --changed tests/test_login.py docs/login.md
python scripts/phase_guard.py --phase green --changed src/login.py
python scripts/phase_guard.py --phase refactor --changed src/login.py
python scripts/phase_guard.py --phase docs --changed README.md docs/login.md
```

3. If the guard fails, stop. Do not rationalize the violation. Move the work into the correct phase.
4. Hand the phase artifact plus the claim to `$review-with-multi-debate`.

Use [references/phase_contracts.md](references/phase_contracts.md) for the exact phase ownership rules and [references/phase_audits.md](references/phase_audits.md) for audit claims.

## Audit Integration

Each audit should hand `$review-with-multi-debate`:

- the artifact for the phase
- the exact claim text from [references/phase_audits.md](references/phase_audits.md)
- the `feature_name`
- the phase label

Recommended audit phases:

- `request_map`
- `red`
- `green`
- `regression`
- `refactor`
- `docs`
- `final`

Keep the phase artifact compact. Good artifacts are:

- requirement map plus chosen test seam
- failing test output
- diff plus targeted passing test output
- full suite results
- refactor diff plus full suite results

For request-map, red, and final audits, also include:

- the chosen execution path and the observable evidence that proves the path crosses the claimed boundary
- if lower-level tests are claimed to be sufficient, the `strace` or `dtruss` output that shows no high-risk boundary was crossed on the minimal execution path
- if the path does not prove traversal of the risky boundary, red is incomplete even if the test fails as expected

## Resources

- Use [scripts/trace_boundary_check.py](scripts/trace_boundary_check.py) to run `strace` or `dtruss` on a minimal execution path and emit JSON evidence about process, network, and filesystem boundary crossings.
- Open [references/phase_contracts.md](references/phase_contracts.md) when you need exact edit-boundary rules.
- Open [references/phase_audits.md](references/phase_audits.md) when preparing a phase audit with `$review-with-multi-debate`.
- Use [scripts/phase_guard.py](scripts/phase_guard.py) for the monitor agent's scope check.
- Use [evals/evals.json](evals/evals.json) to benchmark whether the skill triggers on the right work and stays lean.
