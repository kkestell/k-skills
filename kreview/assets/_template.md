# Review title

Delete unused headings and placeholder text, including this guidance. List findings fixed during the review under Fixed. Report each open finding under its severity heading, then under its category heading. Omit severity and category headings that have no findings.

Severity describes the cost of leaving the finding unfixed. The levels, most severe first:

- `high` — wrong results, lost or corrupted data, a crash, or a security hole that normal use can trigger.
- `medium` — wrong behavior that only an uncommon but realistic case triggers, or code that makes future changes materially riskier or more expensive.
- `low` — no effect on behavior and little effect on future changes, such as unclear naming, stale comments, or minor duplication.

Categories:

- `correctness` — required behavior and reachable state changes.
- `error-handling` — failures, useful errors, cancellation, and partial effects.
- `resources` — resource ownership, lifetime, and cleanup.
- `concurrency` — shared state, task lifetime, and cancellation.
- `security` — trust boundaries, permissions, and secrets.
- `performance` — material costs for realistic inputs.
- `api-design` — caller contracts and shared interfaces.
- `architecture` — responsibilities, dependencies, and needless complexity.
- `dependencies` — library choices and integration costs.
- `simplicity` — less code and fewer concepts with behavior preserved.
- `readability` — clear control flow and local reasoning.
- `naming` — clear and consistent vocabulary.
- `comments` — useful explanations of intent, constraints, and consequences in the code.
- `documentation` — caller guidance and design documents associated with the code under review.
- `testing` — behavior coverage and reliable assertions.

## Scope and coverage

State what you reviewed and any material gaps in coverage.

## Fixed

For each finding fixed during the review, give the source location, what could happen, and the fix.

- **Finding title** (`path/to/file.rs:line`): Consequence and fix.

## Findings

For each open finding, give its title, the source location, what can happen, the evidence, and a suggested fix. If there are no open findings, say so here.

### Severity

#### Category

- **Finding title** (`path/to/file.rs:line`): Consequence, evidence, and fix.

## Checks run

List the checks you actually ran and their results.

## Verdict

Summarize the review result and any action needed.
