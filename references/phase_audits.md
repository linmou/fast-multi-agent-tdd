# Intent

Provide exact claim text for mandatory debate audits and lightweight phase gates so agents judge concrete artifacts instead of fuzzy stories.

## Request Map Claim

Claim:
`The request map decomposes the work into testable requirements, picks the smallest next slice, and defines a phase-safe TDD path.`

Default handling:
Record this artifact for the Red and cumulative Refactor audits. Do not run `$review-with-multi-debate` for request-map by default.

Suggested criteria:

- requirements are concrete and testable
- the chosen slice is the smallest sensible increment
- the proposed test level matches the behavior under change
- the next phases can proceed without mixing test and production edits

## Red Claim

Claim:
`The red phase adds only the next failing test, and the failure is caused by missing behavior rather than syntax, environment, or unrelated breakage.`

Suggested criteria:

- changed files belong to red
- the test is the smallest useful specification step
- the failure output points to missing behavior
- no production code was changed

## Green Gate Claim

Claim:
`The green phase changed only production/runtime files, did not edit tests, made the targeted red test pass, and saved the production diff for cumulative review.`

Suggested criteria:

- changed files belong to green
- the targeted red test now passes
- tests remained untouched
- the production diff is saved for the cumulative Refactor audit

Default handling:
Use the monitor scope check, changed-file list, targeted test output, and saved diff. Do not run `$review-with-multi-debate` for Green by default.

## Regression Claim

Claim:
`The regression check ran the full available suite after the green change, and the results show no new unrelated failures or flakiness.`

Suggested criteria:

- targeted tests passed before the full suite
- the full suite was run or the blocker is explicitly documented
- failures, if any, are analyzed rather than ignored
- repeated runs do not show flakiness

Default handling:
Record targeted and full-suite output for the cumulative Refactor audit. Do not run `$review-with-multi-debate` for regression by default.

## Cumulative Refactor Claim

Claim:
`The final production diff from pre-Green to post-Refactor implements only the behavior required by the request map and red tests, avoids speculative logic or hidden fallbacks, preserves passing regression results, and leaves the code simpler or no worse than before.`

Suggested criteria:

- changed files belong to refactor
- the suite stayed green after refactoring
- the cumulative production diff matches the request map and red tests
- the refactor-only diff does not introduce new behavior
- the change reduces duplication, indirection, or naming debt
- hidden fallback, retry, broad rewrite, or unrelated public behavior changes are absent
- no test files were edited

## Docs Claim

Claim:
`The documentation phase updates only docs relevant to the completed code change, keeps the docs aligned with implemented behavior, and does not edit tests or production code.`

Default handling:
Record the docs artifact for final closeout. Do not run `$review-with-multi-debate` for docs by default.

Suggested criteria:

- changed files belong to docs
- the docs describe behavior that the code now implements
- no production or test files were edited in this phase
- the doc delta is narrow rather than a speculative redesign

## Final Claim

Claim:
`The completed work preserves strict TDD discipline, covers each mapped requirement with passing tests, updates relevant docs after TDD is complete, and clearly reports remaining risks.`

Default handling:
Use this for final closeout. Do not run `$review-with-multi-debate` for final by default.

Suggested criteria:

- every requirement has a passing test
- red audit, green gate, regression, cumulative refactor audit, and docs artifacts exist when docs were relevant
- phase violations were either absent or corrected explicitly
- remaining risks are concrete and small
