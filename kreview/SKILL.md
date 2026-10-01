---
name: kreview
description: "Review code in a diff, branch, commit, or specified files, fix findings that have obvious fixes, write the review of the remaining findings in `agents/reviews/`, and commit. Do not use for plan critiques or standalone documentation reviews."
argument-hint: "[review scope]"
---

## Objective

Review the code the user names. Fix findings that have an obvious, straightforward fix, report the rest, and commit. Follow review and delegation rules in `AGENTS.md`.

This skill and `agents/reviews/` are for code reviews. Plan critiques and standalone documentation reviews are outside its scope. Read plans and documentation as context for code under review.

## Choose what to review

Read `<input_document> $ARGUMENTS </input_document>`. Ask for clarification only when the answer would change what you review.

For a diff, branch, or commit, inspect its changes and the code that calls or depends on them. For named files, directories, or the whole codebase, review that full scope. For a feature review, check other code the feature needs, even when it is outside the diff.

## Review

Trace behavior through callers, state changes, resource lifetimes, and tests. Judge implementation choices by their purpose and consequence. Do not treat a language feature or coding pattern as a defect on its own.

Read the requirements that define the behavior. If the user has approved a new design, review against that design. Flag complex or expensive code that adds no required behavior.

Confirm each suspected bug by tracing the code, reproducing the behavior, or running a focused check before reporting it. If you cannot confirm it, leave it out. Follow `AGENTS.md` when choosing validation. Do not require a fixed set of commands, and stay within the requested scope. Say when you reviewed only part of the code.

## Fix

Fix a finding when the fix is obvious and straightforward: it has one clear right answer and needs no design, behavior, or interface decision. Leave a finding open when it needs an engineering decision, a design change, or a plan. Make only the change the finding calls for. Validate the fixes as `AGENTS.md` directs. If a fix fails validation and the cause is not obvious, revert it and leave the finding open.

## Report

Read `agents/reviews/_template.md`, or this skill's `assets/_template.md` if the workspace has none, and use it to write the review in `agents/reviews/YYYY-MM-DD-NNN-slug.md`, using the next sequence for the day. State the scope and significant gaps in coverage. List the fixed findings with the source location, what could happen, and the fix. Group open findings by the template's severity levels, most severe first, then by its categories within each severity. For each open finding, give its title, the source location, what can happen, the evidence, and a suggested fix. Record the checks you ran. If there are no findings, say so. End with a short verdict.

## Commit

Commit the fixes and the review together, following the commit rules in `AGENTS.md`. Do not commit unrelated changes. Give the final response and stop.

## Final response

When the review is committed, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the checks that passed, the suspected bugs you ruled out, and the steps you took.

```markdown
One or two sentences giving the verdict, the number of findings fixed, and the number left open by severity.

| Severity | Title                           | Location           |
| -------- | ------------------------------- | ------------------ |
| high     | Parser drops the final token    | `src/parser.rs:42` |
| medium   | Retry loop hides the real error | `src/fetch.rs:88`  |

**Review:** `agents/reviews/YYYY-MM-DD-NNN-slug.md` · **Commit:** `abc1234`

**Files:**

- `src/parser.rs` (modified)
- `agents/reviews/YYYY-MM-DD-NNN-slug.md` (created)

**Next:** `/kplan fix "Parser drops the final token" from agents/reviews/YYYY-MM-DD-NNN-slug.md`
```

The table lists the open findings at every severity level, most severe first. If there are none, replace the table with `No open findings.` List every file the commit created or modified, marked `(created)` or `(modified)`. For Next, recommend planning the fix for the most severe open finding. If the table has no findings, write `None.`
