---
name: kwork
description: Implement a plan from `agents/plans/` and stage the changes for review. Use to carry out a written plan, not to plan or review.
argument-hint: "[plan path or slug]"
---

## Objective

Implement the plan and stage the changes for review.

## Establish the work

1. Read `<plan> $ARGUMENTS </plan>` and find the plan in `agents/plans/`. If it is empty or matches no plan, ask which plan to implement and stop.
2. Read the plan.

## Implement

3. Read the code the plan references before changing it. Carry out the plan's tasks in order and write the tests it names.
4. Use the names the plan gives. Do not add work the plan does not call for.
5. When the code contradicts the plan or a task cannot be done as written, make the smallest departure that still meets the plan's goal and report it under Surprises. Do not redesign the change.
6. Validate the change. Fix failures before continuing.

## Stage

7. Stage the implementation and the plan. Do not stage unrelated changes. Do not commit; `/kreview` commits the work when no findings remain open.
8. Give the final response and stop.

## Final response

When the work is staged, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the checks that passed and the steps you took.

```markdown
One or two sentences saying what was built and whether the plan's goal is met.

**Surprises:**

- A departure from the plan, a detour, something unexpected in the code, or follow-up work.

**Lines:** +120 / −45 (net +75)

**Files:**

- `src/parser.rs` (modified)
- `src/tokens.rs` (created)
- `agents/plans/YYYY-MM-DD-NNN-slug.md` (created)

**Next:** `/kreview staged changes for agents/plans/YYYY-MM-DD-NNN-slug.md`
```

Write `None.` under Surprises if the work went as planned. Count lines from the staged changes, excluding `agents/`, with `git diff --cached --shortstat -- . ':(exclude)agents'`. List every staged file, marked `(created)` or `(modified)`.
