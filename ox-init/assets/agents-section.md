## Ox workflow

Plans, work logs, reviews, and issues live in `agents/`.

- `/ox-plan` explores a change and writes a plan to `agents/plans/`.
- `/ox-work` implements a plan, writes a work log to `agents/work/`, and commits.
- `/ox-review` reviews code, fixes findings that have obvious fixes, writes a review to `agents/reviews/`, records the remaining findings in `agents/issues.csv`, checks off the reviewed task in `agents/todo.md`, and commits.
- `agents/todo.md` is the task list. High and medium severity issues are added under the task they affect, or as new top-level items.
- `agents/issues.csv` is the issue log. Each row has an id (`OX-NNNN`), a created time, a title, a severity (`low`, `medium`, `high`), the review lens that found it, a status (`unscheduled`, `scheduled`, `wontfix`, `fixed`), and the review that found it. Issues found outside a review leave the lens and review empty. Append rows; never reorder or delete them, because `todo.md` links to rows by line number.
