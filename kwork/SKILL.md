---
name: kwork
description: Implement a plan from `agents/plans/`, write a work log in `agents/work/`, and commit. Use to carry out a written plan, not to plan or review.
argument-hint: "[plan path or slug]"
---

## Objective

Implement the plan, record what was done, and commit.

## Establish the work

1. Read `<plan> $ARGUMENTS </plan>` and find the plan in `agents/plans/`. If it is empty or matches no plan, ask which plan to implement and stop.
2. Read the plan.

## Implement

3. Read the code the plan references before changing it. Carry out the plan's tasks in order and write the tests it names.
4. Use the names the plan gives. Do not add work the plan does not call for.
5. When the code contradicts the plan or a task cannot be done as written, make the smallest departure that still meets the plan's goal and record it in the work log. Do not redesign the change.
6. Validate the change. Fix failures before continuing.

## Write the work log

7. Read `agents/work/_template.md`, or this skill's `assets/_template.md` if the workspace has none, and use it to write the work log in `agents/work/`. Name the file `YYYY-MM-DD-NNN-slug.md`, using today's date, the next sequence for the day, and the plan's slug.
8. Keep the log concise. Record where the work departed from the plan and why, decisions made during the work, the checks that ran, manual verification with the commands to reproduce it, and follow-up work. Do not repeat the plan, the diff, or the conversation.

## Commit

9. Commit the implementation and the work log together. If the plan is not already committed, include it in the same commit. Do not commit unrelated changes.
10. Give the final response and stop.

## Final response

When the work is committed, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the checks that passed and the steps you took.

```markdown
One or two sentences saying what was built and whether the plan's goal is met.

**Surprises:**

- A departure from the plan, a detour, something unexpected in the code, or follow-up work.

**Work log:** `agents/work/YYYY-MM-DD-NNN-slug.md` · **Commit:** `abc1234` · **Lines:** +120 / −45 (net +75)

**Files:**

- `src/parser.rs` (modified)
- `src/tokens.rs` (created)
- `agents/work/YYYY-MM-DD-NNN-slug.md` (created)

**Next:** `/kreview commit abc1234`
```

Write `None.` under Surprises if the work went as planned. Count lines from the commit, excluding `agents/`, with `git diff --shortstat HEAD~1 HEAD -- . ':(exclude)agents'`. List every file the commit created or modified, marked `(created)` or `(modified)`.
