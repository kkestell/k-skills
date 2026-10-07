---
name: kreview
description: "Review code in staged changes, a diff, branch, commit, or specified files, fix findings that need no user decision or plan, write a review of the fixed and remaining findings in `agents/reviews/`, and commit the staged work when no findings remain open. Do not use for plan critiques or standalone documentation reviews."
argument-hint: "[review scope]"
---

## Objective

Review the code the user names. Fix every finding that needs no decision from the user and no plan, report the rest, and commit when no findings remain open.

This skill and `agents/reviews/` are for code reviews. Plan critiques and standalone documentation reviews are outside its scope. Read plans and documentation as context for code under review.

## Choose what to review

1. Read `<review_scope> $ARGUMENTS </review_scope>`. Ask for clarification only when the answer would change what you review.
2. For staged changes, a diff, a branch, or a commit, inspect the changes and the code that calls or depends on them. For named files, directories, or the whole codebase, review that full scope. For a feature review, check other code the feature needs, even when it is outside the diff.

## Review

3. Trace behavior through callers, state changes, resource lifetimes, and tests. Judge implementation choices by their purpose and consequence. Do not treat a language feature or coding pattern as a defect on its own.
4. Read the requirements that define the behavior. If the user has approved a new design, review against that design. Flag complex or expensive code that adds no required behavior.
5. Confirm each suspected bug by tracing the code, reproducing the behavior, or running a focused check before reporting it. If you cannot confirm it, leave it out. Choose checks that fit the repository. Do not require a fixed set of commands, and stay within the requested scope. Say when you reviewed only part of the code.

## Fix

6. Fix every finding you can resolve without a decision from the user and without a plan. Use requirements, existing plans, and approved decisions to establish the intended behavior before deciding a fix needs a new decision. Leave a finding open only when a behavior, design, or interface choice remains unresolved, or the change needs substantial implementation planning. Severity and file count alone do not require a plan. Make only the change the finding calls for.
7. Validate the fixes. If a fix fails validation and the cause is not obvious, revert it and leave the finding open.

## Report

8. Read `agents/reviews/_template.md`, or this skill's `assets/_template.md` if the workspace has none, and use it to write the review in `agents/reviews/`. Name the file `YYYY-MM-DD-NNN-slug.md`, using the next sequence for the day.
9. State the scope and significant gaps in coverage. List the fixed findings with the source location, what could happen, and the fix. Group open findings by the template's severity levels, most severe first, then by its categories within each severity. For each open finding, give its title, the source location, what can happen, the evidence, a suggested fix, and the decision it needs or why it needs a plan. Record the checks you ran. If there are no findings, say so. End with a short verdict.

## Commit

10. Stage the fixes and the review. Do not stage unrelated changes.
11. If no findings remain open, commit everything staged in one commit, including any plan and work log staged by `/kwork`. If any finding remains open, do not commit; leave the changes staged.
12. Give the final response and stop.

## Final response

When the review is committed or staged, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the checks that passed, the suspected bugs you ruled out, and the steps you took.

```markdown
One or two sentences giving the verdict, the number of findings fixed, and the number left open by severity.

**Fixed:**

- Unclosed file handle on early return (`src/fetch.rs:31`)

**Open:**

| Severity | Title                           | Location           |
| -------- | ------------------------------- | ------------------ |
| high     | Parser drops the final token    | `src/parser.rs:42` |
| medium   | Retry loop hides the real error | `src/fetch.rs:88`  |

**Review:** `agents/reviews/YYYY-MM-DD-NNN-slug.md` · **Commit:** `abc1234`

**Files:**

- `src/fetch.rs` (modified)
- `agents/reviews/YYYY-MM-DD-NNN-slug.md` (created)

**Next:** `/kplan fix "Parser drops the final token" and "Retry loop hides the real error" from agents/reviews/YYYY-MM-DD-NNN-slug.md`
```

Under Fixed, list each finding fixed during the review with its title and location. If there are none, write `None.` The Open table lists the open findings at every severity level, most severe first. If there are none, replace the table with `None.` If you did not commit, write `**Commit:** None (changes staged)`. List every file in the commit or left staged, marked `(created)` or `(modified)`. For Next, recommend one `/kplan` that covers every open finding, naming each by title. If there are no open findings, write `None.`
