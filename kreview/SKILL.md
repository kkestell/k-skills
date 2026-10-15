---
name: kreview
description: "Review code in staged changes, a diff, branch, commit, or specified files without changing it, write a review in `agents/reviews/` that marks each finding as trivially fixable or not, and commit the staged work when there are no findings. Do not use for plan critiques or standalone documentation reviews."
argument-hint: "[review scope]"
---

## Objective

Review the code the user names and report every finding, marking whether its fix is trivial or needs a decision or a plan. Do not fix anything. Commit when there are no findings.

This skill and `agents/reviews/` are for code reviews. Plan critiques and standalone documentation reviews are outside its scope. Read plans and documentation as context for code under review.

## Choose what to review

1. Read `<review_scope> $ARGUMENTS </review_scope>`. Ask for clarification only when the answer would change what you review.
2. For staged changes, a diff, a branch, or a commit, inspect the changes and the code that calls or depends on them. For named files, directories, or the whole codebase, review that full scope. For a feature review, check other code the feature needs, even when it is outside the diff.

## Review

3. Trace behavior through callers, state changes, resource lifetimes, and tests. Judge implementation choices by their purpose and consequence. Do not treat a language feature or coding pattern as a defect on its own.
4. Read the requirements that define the behavior. If the user has approved a new design, review against that design. Flag complex or expensive code that adds no required behavior.
5. Confirm each suspected bug by tracing the code, reproducing the behavior, or running a focused check before reporting it. If you cannot confirm it, leave it out. Choose checks that fit the repository. Do not require a fixed set of commands, and stay within the requested scope. Say when you reviewed only part of the code. Do not change the code under review. Revert any edit a check needs before you finish.

## Classify

6. Mark each finding's fix with one of three labels:
   - `Trivial`: the fix needs no decision from the user and no plan.
   - `Needs decision`: a behavior, design, or interface choice remains unresolved.
   - `Needs plan`: the change needs substantial implementation planning.

   Use requirements, existing plans, and approved decisions to establish the intended behavior before deciding a fix needs a new decision. Severity and file count alone do not make a fix non-trivial.

## Report

7. Read `agents/reviews/_template.md`, or this skill's `assets/_template.md` if the workspace has none, and use it to write the review in `agents/reviews/`. Name the file `YYYY-MM-DD-NNN-slug.md`, using the next sequence for the day.
8. State the scope and significant gaps in coverage. Give every finding an ID in severity order, most severe first, and list it in the summary table with its fix label. Give each finding its own section with its severity, category, fix label, source location, what can happen, the evidence, and the fix. For a `Trivial` finding, the fix is the exact change. For the others, it is a suggested fix and the decision it needs or why it needs a plan. Record the checks you ran. If there are no findings, say so. End with a short verdict.

## Commit

9. Stage the review. Do not stage anything else.
10. If there are no findings, commit everything staged in one commit, including the plan staged by `/kplan` and the work staged by `/kwork`. If there are findings, do not commit; leave the changes staged.
11. Give the final response and stop.

## Final response

When the review is committed or staged, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the checks that passed, the suspected bugs you ruled out, and the steps you took.

```markdown
One or two sentences giving the verdict and the number of findings by severity, and how many are trivial.

| ID | Severity | Fix            | Title                           | Location           |
| -- | -------- | -------------- | ------------------------------- | ------------------ |
| F1 | High     | Needs decision | Parser drops the final token    | `src/parser.rs:42` |
| F2 | Medium   | Trivial        | Retry loop hides the real error | `src/fetch.rs:88`  |

**Review:** `agents/reviews/YYYY-MM-DD-NNN-slug.md` · **Commit:** `abc1234`

**Files:**

- `agents/reviews/YYYY-MM-DD-NNN-slug.md` (created)

**Next:** `/kplan fix F1 and F2 from agents/reviews/YYYY-MM-DD-NNN-slug.md`
```

The table lists every finding, most severe first. If there are none, replace the table with `No findings.` If you did not commit, write `**Commit:** None (changes staged)`. List every file in the commit or left staged, marked `(created)` or `(modified)`. For Next, recommend one `/kplan` that covers every finding, naming each by ID. If there are no findings, write `None.`
