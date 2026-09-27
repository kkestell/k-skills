---
name: ox-init
description: "Create `agents/todo.md` and `agents/issues.csv` if they are missing and describe the Ox workflow in `AGENTS.md`. Use when setting up the Ox skills in a repository."
---

## Objective

Set up the files the Ox skills share. Do not overwrite anything that already exists.

## Create the workflow files

1. Create `agents/` if it does not exist.
2. If `agents/todo.md` does not exist, copy this skill's `assets/todo.md` there.
3. If `agents/issues.csv` does not exist, copy this skill's `assets/issues.csv` there. It contains only the header row.

## Document the workflow

4. Read `AGENTS.md` at the repository root, or create it if it is missing.
5. If it does not already describe the Ox workflow, add the section in this skill's `assets/agents-section.md`. Keep it concise and adjust paths only if the repository keeps these files elsewhere. If the workflow is already described, leave it as is.

## Final response

When setup is done, reply in the form below and nothing else. Lead with the main point, write plainly, and leave out the checks that passed and the steps you took.

```markdown
One sentence saying what was set up, or that the Ox workflow was already in place.

**Files:**

- `agents/todo.md` (created)
- `AGENTS.md` (modified)
```

List every file you created or modified, marked `(created)` or `(modified)`. If you changed nothing, omit the Files list.
