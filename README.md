# K Skills

## Skills

Each artifact directory may contain a `_template.md`; if it does, the skill uses it, otherwise the skill falls back to its built-in default template.

### `/kplan`

Plans a code or behavior change. Writes a plan to `agents/plans/`.

### `/kwork`

Implements a plan. Stages the plan and code changes without committing.

### `/kdiscuss <claude|codex|opencode> <topic or artifact path>`

Refines a plan, argument, or idea with another agent in a persistent conversation. Updates supplied plans with agreed improvements and reports unresolved questions. Uses Claude Code with Opus 5.5 and high effort, Codex with GPT-6.1 Sol and high effort, or OpenCode with DeepSeek V4.1 Flash from the DeepSeek provider and max effort. Requires the selected CLI and its authentication to be configured.

### `/kreview`

Reviews code in a diff, branch, commit, or files. Fixes findings that need no user decision or plan, writes a review of the fixed and remaining findings to `agents/reviews/`, and stages it. Commits everything staged when no findings remain open; otherwise leaves the changes staged and recommends `/kplan` for the open findings.

## Workflows

Run each step in a fresh session.

### Implement a task

1. `/kplan add CSV export`
2. `/kwork agents/plans/2026-09-25-001-export.md`
3. `/kreview staged changes for agents/plans/2026-09-25-001-export.md`

The plan, code changes, and review land in one commit when the review leaves no findings open.

### Fix review findings that need a plan

1. `/kplan fix "Parser drops the final token" and "Retry loop hides the real error" from agents/reviews/2026-09-25-001-export.md`
2. `/kwork agents/plans/2026-09-25-002-fix-review-findings.md`
3. `/kreview staged changes for agents/plans/2026-09-25-002-fix-review-findings.md`

The earlier work stays staged, so the final commit includes both rounds.

### Refine a plan before implementation

1. `/kplan add CSV export`
2. `/kdiscuss claude agents/plans/2026-09-25-001-export.md`
3. `/kwork agents/plans/2026-09-25-001-export.md`

Use `codex` or `opencode` in the discussion step to choose another agent. The initiating agent evaluates each reply and develops the proposal; the helper preserves the other agent's session for up to six replies, including final confirmation.

## Global install

From a local checkout:

```bash
npx skills add /path/to/k-skills -g -a claude-code -a codex -s '*'
```

From GitHub:

```bash
npx skills add kkestell/k-skills -g -a claude-code -a codex -s '*'
```
