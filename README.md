# K Skills

## Skills

Each artifact directory may contain a `_template.md`; if it does, the skill uses it, otherwise the skill falls back to its built-in default template.

### `/kplan`

Plans a code or behavior change. Writes a plan to `agents/plans/`.

### `/kwork`

Implements a plan and commits. Writes a work log to `agents/work/`.

### `/kreview`

Reviews code in a diff, branch, commit, or files. Fixes findings that have obvious fixes, writes a review of the remaining findings to `agents/reviews/`, and commits.

## Workflows

Run each step in a fresh session.

### Implement a task

1. `/kplan add CSV export`
2. `/kwork agents/plans/2026-09-25-001-export.md`
3. `/kreview the last commit`

### Fix a review finding

1. `/kplan fix "Parser drops the final token" from agents/reviews/2026-09-25-001-export.md`
2. `/kwork agents/plans/2026-09-25-002-fix-final-token.md`
3. `/kreview the last commit`

## Global install

From a local checkout:

```bash
npx skills add /path/to/k-skills -g -a claude-code -a codex -s '*'
```

From GitHub:

```bash
npx skills add kkestell/k-skills -g -a claude-code -a codex -s '*'
```
