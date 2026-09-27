---
name: ox-review
description: "Review code in a diff, branch, commit, or specified files, fix findings that have obvious fixes, write the review in `agents/reviews/`, record the remaining findings in `agents/issues.csv`, and commit. Supports general and language-specific focused code reviews. Do not use for plan critiques or standalone documentation reviews."
argument-hint: "[general|lens[,lens...]] [review scope]"
---

## Objective

Review the code the user names. Fix findings that have an obvious, straightforward fix, record the rest as issues, and commit. Follow review and delegation rules in `AGENTS.md`.

This skill and `agents/reviews/` are for code reviews. Plan critiques and standalone documentation reviews are outside its scope. Read plans and documentation as context for code under review; the documentation lens checks guidance for that code.

## Standard

The code under review is a personal project with one user, its author. Small, direct code that is easy to understand matters more than handling every case. Report only what would actually go wrong for that user, or what makes the code harder to understand or larger than it needs to be.

These are not findings:

- Inputs the user will not produce, adversarial inputs, or data the program itself wrote that could only be malformed if something else had already failed.
- Multiple users, concurrent access, or hostile networks, unless the code actually does that.
- Resource exhaustion, hardening, or a defensive check whose only justification is that the case is possible in theory.
- A missing recovery path where crashing with a clear message is acceptable.
- A style or pattern preference with no effect on behavior or readability.

Existing code that handles one of these cases is a finding: report it as code to remove.

Severity describes the effect on the user:

- `high` — wrong results, lost data, or a crash in normal use.
- `medium` — wrong behavior in a realistic case, or code that is materially harder to understand or larger than it needs to be.
- `low` — polish.

## Choose what to review

Read `<input_document> $ARGUMENTS </input_document>`. Use `general` unless the user names one or more lenses from the list below. Ask for clarification only when the answer would change what you review.

For a diff, branch, or commit, inspect its changes and the code that calls or depends on them. For named files, directories, or the whole codebase, review that full scope. For a feature review, check other code the feature needs, even when it is outside the diff.

For a general review, choose lenses that fit the code and its risks, including language-specific lenses when applicable. For a focused review, stay within the requested lenses and examine the relevant code closely. Read only the matching lens files linked below. Each lens is either general or specific to one language.

## Review

Trace behavior through callers, state changes, resource lifetimes, and tests. Judge implementation choices by their purpose and consequence. Do not treat a language feature or coding pattern as a defect on its own.

Read the requirements that define the behavior. If the user has approved a new design, review against that design. Flag complex or expensive code that adds no required behavior. Do not recommend extra code for a hypothetical edge case alone.

Confirm each suspected bug by tracing the code, reproducing the behavior, or running a focused check before reporting it. If you cannot confirm it, leave it out. Follow `AGENTS.md` when choosing validation. A lens does not require a fixed set of commands, a new test for each error path, or a broader review than the requested scope. Say when you reviewed only part of the code.

## Fix

Fix a finding when the fix is obvious and straightforward: it has one clear right answer and needs no design, behavior, or interface decision. Leave a finding open when it needs an engineering decision, a design change, or a plan. Make only the change the finding calls for. Validate the fixes as `AGENTS.md` directs. If a fix fails validation and the cause is not obvious, revert it and leave the finding open.

## Report

If `agents/issues.csv` or `agents/todo.md` is missing, run the `ox-init` skill first. Read `agents/issues.csv` and give each open finding the next unused id (`OX-NNNN`, one more than the highest id in the file).

Read `agents/reviews/_template.md`, or this skill's `assets/_template.md` if the workspace has none, and use it to write the review in `agents/reviews/YYYY-MM-DD-NNN-slug.md`, using the next sequence for the day. State the scope, selected lenses, and significant gaps in coverage. List the fixed findings with the source location, what could happen, and the fix; they get no id. Group open findings by severity (high, medium, low), then by lens within each severity. For each open finding, give its id, the source location, what can happen, the evidence, and a suggested fix. Record the checks you ran. If there are no findings, say so. End with a short verdict.

## Record issues

Append one row to `agents/issues.csv` for each open finding, in the order they appear in the review. Fixed findings stay out of `issues.csv` and `todo.md`. Never reorder or delete existing rows, because `todo.md` links to rows by line number. Quote a field that contains a comma, a quote, or a newline as CSV requires. The columns are:

- `id` — the finding's `OX-NNNN` id.
- `created` — the current local date and time as `YYYY-MM-DD HH:MM`.
- `title` — the finding title.
- `severity` — `high`, `medium`, or `low`.
- `lens` — the lens that found it, or empty.
- `status` — `scheduled` for high and medium severity, `unscheduled` for low.
- `review` — the review path relative to `agents/`, such as `reviews/2026-09-25-001-slug.md`.

Add each high and medium severity issue to `agents/todo.md` as an unchecked item, `- [ ] [OX-NNNN](issues.csv:LINE): Title`, where `LINE` is the row's line number in `issues.csv`. When the user, the plan, or the work log for the reviewed change names a task in `todo.md`, nest the item under that task. Otherwise add it as a new top-level item. Low severity issues stay out of `todo.md`.

## Update the task

When the user, the plan, or the work log for the reviewed change names a task in `todo.md`, check that task off. Issues nested under it stay unchecked. If the task links to an issue, set that issue's status to `fixed` in `issues.csv`.

## Commit

Commit the fixes, the review, `issues.csv`, and `todo.md` together, following the commit rules in `AGENTS.md`. Do not commit unrelated changes. Give the final response and stop.

## General lenses

`general` is the review mode that chooses applicable lenses; it is not a lens.

- [`resources`](references/general/resources.md) — resource ownership, lifetime, and cleanup.
- [`error-handling`](references/general/error-handling.md) — failures, useful errors, cancellation, and partial effects.
- [`api-design`](references/general/api-design.md) — caller contracts and shared interfaces.
- [`naming`](references/general/naming.md) — clear and consistent vocabulary.
- [`performance`](references/general/performance.md) — material costs for realistic inputs.
- [`testing`](references/general/testing.md) — behavior coverage and reliable assertions.
- [`readability`](references/general/readability.md) — clear control flow and local reasoning.
- [`comments`](references/general/comments.md) — useful explanations of intent, constraints, and consequences in the code.
- [`concurrency`](references/general/concurrency.md) — shared state, task lifetime, and cancellation.
- [`security`](references/general/security.md) — trust boundaries, permissions, and secrets.
- [`correctness`](references/general/correctness.md) — required behavior and reachable state changes.
- [`architecture`](references/general/architecture.md) — responsibilities, dependencies, and needless complexity.
- [`dependencies`](references/general/dependencies.md) — library choices and integration costs.
- [`documentation`](references/general/documentation.md) — caller guidance and design documents associated with the code under review.
- [`simplicity`](references/general/simplicity.md) — less code and fewer concepts with behavior preserved.

## Rust lenses

Use these only for Rust code. Future language lenses belong in their own language directory, with no language-specific rules in general lenses.

- [`rust-ownership`](references/rust/ownership.md) — borrowing, clones, allocation, and shared ownership.
- [`rust-idioms`](references/rust/idioms.md) — `Result`/`Option`, traits, generics, macros, and Rust concurrency types.
- [`rust-cargo`](references/rust/cargo.md) — Cargo manifests, lockfiles, features, and toolchain costs.

## Final response

When the review is committed, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the checks that passed, the suspected bugs you ruled out, and the steps you took.

```markdown
One or two sentences giving the verdict, the number of findings fixed, and the number left open by severity.

| ID      | Severity | Title                           | Location           |
| ------- | -------- | ------------------------------- | ------------------ |
| OX-0012 | high     | Parser drops the final token    | `src/parser.rs:42` |
| OX-0013 | medium   | Retry loop hides the real error | `src/fetch.rs:88`  |

**Review:** `agents/reviews/YYYY-MM-DD-NNN-slug.md` · **Commit:** `abc1234`

**Files:**

- `src/parser.rs` (modified)
- `agents/reviews/YYYY-MM-DD-NNN-slug.md` (created)
- `agents/issues.csv` (modified)
- `agents/todo.md` (modified)

**Next:** `/ox-plan fix OX-0012 from agents/issues.csv`
```

The table lists the open high and medium severity findings, high first. If there are none, replace the table with `No open high or medium severity findings.` List every file the commit created or modified, marked `(created)` or `(modified)`. For Next, recommend planning the fix for the most severe open finding. If there are no open high or medium severity findings, recommend `/ox-plan` for the first unchecked task in `agents/todo.md`, or write `Nothing left in agents/todo.md.` if there is none.
