# Intent

Provide exact claim text for each phase audit so `$review-with-multi-debate` can judge a concrete artifact instead of a fuzzy story.

## Request Map Claim

Claim:
`The request map decomposes the work into testable requirements, picks the smallest next slice, and defines a phase-safe TDD path.`

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

## Green Claim

Claim:
`The green phase applies the minimum production change needed to satisfy the red-phase test, and it does not edit tests.`

Suggested criteria:

- changed files belong to green
- the targeted red test now passes
- the diff does not contain speculative logic
- tests remained untouched

## Regression Claim

Claim:
`The regression check ran the full available suite after the green change, and the results show no new unrelated failures or flakiness.`

Suggested criteria:

- targeted tests passed before the full suite
- the full suite was run or the blocker is explicitly documented
- failures, if any, are analyzed rather than ignored
- repeated runs do not show flakiness

## Refactor Claim

Claim:
`The refactor phase improves the production code structure without changing behavior, and it does not edit tests.`

Suggested criteria:

- changed files belong to refactor
- the suite stayed green after refactoring
- the change reduces duplication, indirection, or naming debt
- no test files were edited

## Docs Claim

Claim:
`The documentation phase updates only docs relevant to the completed code change, keeps the docs aligned with implemented behavior, and does not edit tests or production code.`

Suggested criteria:

- changed files belong to docs
- the docs describe behavior that the code now implements
- no production or test files were edited in this phase
- the doc delta is narrow rather than a speculative redesign

## Final Claim

Claim:
`The completed work preserves strict TDD discipline, covers each mapped requirement with passing tests, updates relevant docs after TDD is complete, and clearly reports remaining risks.`

Suggested criteria:

- every requirement has a passing test
- red, green, regression, refactor, and docs artifacts exist when docs were relevant
- phase violations were either absent or corrected explicitly
- remaining risks are concrete and small
