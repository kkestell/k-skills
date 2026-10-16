# An Agentic Development Workflow

> The ability to simplify means to eliminate the unnecessary so that the necessary may speak.<br>— Hans Hofmann

This workflow assumes the developer roughly knows what they want to build, is prepared to make the architectural decisions, cares about the code.

There are no agent swarms here -- no worktrees. This is just you, an agent harness, your code, a couple files, and a few agent skills; working carefully on one thing at a time.

Don't forget:

- This stuff changes _fast_. This is my workflow today. It probably won't be my workflow tomorrow. Stay nimble.
- Do what works for you, your team, and your project.
- Don't believe the hype. Nobody has this figured out yet. Use agents to write code, read that code, and form your own opinions.

## Overview

Start by defining the product behavior in `agents/spec.md`, by hand or with `/kspec`, then break it into tasks in `agents/todo.md`.

For each task, the agent writes a plan, implements it, and reviews the changes. You review the plan and make any decisions the agent raises. The plan, code, work log, and review are committed together, then the task is checked off.

![The workflow: Spec (/kspec) writes spec.md, which feeds todo.md, then Plan, Work, Review, and Commit; the task is checked off](workflow.svg)

## The Workflow

### 1. Spec

```
/kspec
```

The spec skill helps you define or update the product's observable behavior. The agent works through open product decisions with you, one question at a time, then writes the settled behavior to `agents/spec.md`. Break that behavior into tasks in `agents/todo.md` before planning the implementation.

Return to `/kspec` when product behavior needs defining or changing. For each task, follow the plan, work, and review cycle below.

### 2. Plan

```
/kplan the next task in agents/todo.md
```

The plan skill takes the next task in `todo.md`. The agent explores the codebase, works through any open design decisions with you, and writes an implementation plan to `agents/plans/`.

Planning upfront forces the agent to confront edge cases before writing code, lets you use a cheaper, faster model for the implementation, and lets you steer the design before bad code is written.

### 3. Work

```
/kwork agents/plans/2026-10-16-001-export.md
```

Once the plan looks right, the work skill takes over. The agent implements the plan, runs the checks, and writes a work log to `agents/work/` recording how the change was verified, where it departed from the plan, and any surprises it ran into.

### 4. Review

```
/kreview staged changes for agents/plans/2026-10-16-001-export.md
```

After the implementation is done, the review skill checks it. The agent reviews the changes against the plan, fixes trivial issues directly, and asks you to decide on anything non-trivial. It writes the review to `agents/reviews/` and commits the plan, code changes, work log, and review together.

## Consistent responses

Each skill has a **Final response** section that specifies the format and information the assistant should include when it finishes. The response summarizes the result and links to the files it produced. Depending on the skill, it also calls out decisions, surprises, or review findings. The plan, work, and review skills include the next command to run.

I've found this consistency really nice. I know where to look for the result, what needs my attention, and which command to run next.

## Project Layout

Start with three files:

```text
.
├── AGENTS.md
└── agents/
    ├── spec.md
    └── todo.md
```

`AGENTS.md` sits at the root of the repository and holds the project's standing instructions for the agent: what the project is, how to run the checks, and a few rules about style, documentation, and communication.

Everything else lives in `agents/`, which keeps the workflow's files together and out of the way of the code:

- **`spec.md`** describes what the project does from the outside: its behavior, its integrations with other systems, and the invariants it must keep. It's the shared definition of what's being built, and tasks are drawn from it.
- **`todo.md`** is the backlog, a list of milestones broken into session-sized tasks. It tracks what comes next.
- **`plans/`** holds one implementation plan per task. Writing the plan before any code lets you steer the design while it's still cheap to change.
- **`work/`** holds one work log per task, recording how the change was verified, where it departed from the plan, and decisions made along the way.
- **`reviews/`** holds one code review per task, with the findings and how each was resolved.

Some projects might also need an `agents/architecture.md`, covered below.

The plan, work, and review skills each include a built-in template for the files they produce. To customize those formats for a project, add an `_template.md` file in the corresponding directory:

- `agents/plans/_template.md`
- `agents/work/_template.md`
- `agents/reviews/_template.md`

Each skill uses the project's template when present and its built-in template otherwise.

### `AGENTS.md`

> The more you tighten your grip, Tarkin, the more star systems will slip through your fingers.<br>— Princess Leia Organa

Keep `AGENTS.md` short. The agent reads these instructions on every task, so every rule takes attention away from the code and the problem you're trying to solve. A long list also makes it harder for you to tell which rules are helping.

Many rules are workarounds for quirks in a particular model. The next model may handle those things on its own, but the old rules tend to stick around. Over time, you can end up with instructions that mostly tell the agent what it would have done anyway. Start with very few, read the code it produces, and add rules when you see recurring problems. Revisit those rules when you change models.

Here's an example:

````markdown
# Project

Describe your project in one sentence.

## Commands

- `npm run lint` runs every check.
- ...

## Workspace

```text
.
├── AGENTS.md
├── agents/
│   ├── spec.md           # Project behavior, integrations, and invariants
│   ├── architecture.md   # Constraints and design decisions (optional)
│   ├── todo.md           # Milestones and tasks
│   ├── plans/            # Implementation plans
│   ├── work/             # Work logs and verification results
│   └── reviews/          # Code reviews and finding resolutions
├── src/
└── tests/
```

## Style

- Do less. Keep correct code simple, idiomatic, and cheap to change.
- Give each concern a clear boundary and each lifecycle one owner.
- Solve the actual problem. Every addition must justify its complexity; producing more code is not a goal. When both a simple solution and a general solution work, choose the simple one and wait for evidence before generalizing.
- Test observable behavior. Use a small number of representative examples and meaningful regression tests for actual bugs.

## Documentation

- Give each fact a single source of truth.
- The code and its comments describe the implementation. Git history records changes.
- Most code needs no comments. Most changes need no documentation updates.
- Do not create new documentation files or sections unless requested.
- Code, comments, and test names describe the project in its own terms. Never mention roadmap milestones, ticket numbers, plans, or other work records in them.

## Communication

- Describe things directly, clearly, and plainly. Lead with the main point, then add detail as needed.
- Avoid jargon, invented terms, and shorthand. Never mix definitions or overload terms.
- Explain what changed and how it was verified. Be short. Say the thing and stop.
````

The documentation rules keep agents from filling the repository with explanations of code they just wrote. Left alone, agents often produce summaries, walkthroughs, and other documents that mostly restate the implementation. Those files cost tokens to write and read, need updating when the code changes, and can mislead the next session when they fall out of date.

The agent can read the code directly. Removing documentation that merely repeats it usually doesn't make the agent's work any worse. Keep documentation for what the code can't explain: intended behavior, constraints that span the project, and the reasons behind design decisions.

### `agents/spec.md`

Start with `agents/spec.md`, written by hand or with the agent. It defines what the project does, how it interacts with other systems, and the rules its behavior must satisfy. Keep implementation details in the code.

For a specific behavior change, give `/kspec` a focused request:

```
/kspec define how task exports should handle filters and empty results
```

Write enough to guide the first tasks, then refine the spec as you build and learn. Use `/kspec` again when product behavior changes; `/kplan` handles how to implement it.

### `agents/todo.md`

Once some or all of the spec is written, it's broken into milestones and tasks in `todo.md`. It's just a simple two-level list:

- **Milestones:** A large feature or subsystem.
  - **Tasks:** Session-sized units of work that are implemented in sequence, reasonably self-contained (the project builds after each task), and meaningfully testable.

```markdown
# Todo

- Tasks API
  - [x] Create and fetch tasks in memory
  - [x] List tasks and filter them by status
  - [ ] Update and delete tasks
- Persistence
  - [ ] Add a PostgreSQL task store behind the in-memory store's interface
  - [ ] Run the service against PostgreSQL, reading `DATABASE_URL` at startup
```

Check off tasks as you finish them to track progress within each milestone. Milestones don't have checkboxes: remove them from `todo.md` when all their tasks are done. This keeps the backlog focused on upcoming work; the plans, work logs, reviews, and commit history preserve the record of completed work.

### `agents/architecture.md` (optional)

`architecture.md` documents the project's implementation constraints and the reasoning behind key design decisions. It covers dependency boundaries, ownership of shared state and resources, and how work is split across threads or processes.

This file can easily accumulate cruft, so keep it focused on high-level architecture. Do not let it become a running commentary on the code. Most code changes shouldn't touch it; update it only when the architecture changes. Include it only when the project needs these rules and decisions documented.

## Models and harnesses

The skills are written to work across Claude Code, Codex, and OpenCode, so you can switch harnesses and models without changing the workflow. You don't have to use the same model for every step. You might use a stronger model to work through the design, then a cheaper, faster one to implement the plan.

It's worth using a different model for review. The model that wrote the code may repeat the assumptions it made during implementation; another model may question those assumptions or catch mistakes the first one missed. You still need to read the code and judge the findings yourself.

## Sessions

The spec, to-do, plan, and work can all happen in a single session, as long as you keep an eye on the context window. Other times it makes sense to split things up: the spec and to-do in one session, then plan, work, and review each in a fresh session.

The trade-off is that the agent has to reorient itself at the start of every fresh session. Prefix caching makes long sessions much, much cheaper than they look.

## Examples

Here are a few projects built with this workflow. Their repositories show what the generated plans, work logs, reviews, and commit histories look like in practice:

- **[Ox](https://github.com/kkestell/ox)**: An ACP-native coding agent in Go, with an ACP server and a terminal UI.
- **[Willow](https://github.com/kkestell/willow)**: A small, statically typed language with Python-like syntax that compiles to Lua and runs on LuaJIT.

## Claude Code Tips and Tricks

### No Free Advertising

Disable Claude's attribution in commits and pull requests:

```json
{
  "includeCoAuthoredBy": false
}
```

See the [attribution settings](https://code.claude.com/docs/en/settings-reference#includecoauthoredby).

### Spinner Verbs

`"mode": "replace"` replaces the default spinner verbs with your own. Use `"append"` to keep the defaults too. Here's my full list:

```json
{
  "spinnerVerbs": {
    "mode": "replace",
    "verbs": [
      "DISTILLING A CHINESE MODEL",
      "PERPETUAL MOTION IS POWERED BY CUBIC WISDOM",
      "RELOCATING THE EYES OF THE FLOUNDER FISH",
      "GENE RAY IS NOT A CRACKPOT",
      "BE THREE FEET BEHIND YOUR HEAD"
    ]
  }
}
```

### Disable Artifacts

Turn off Claude Code's Artifact tool:

```json
{
  "enableArtifact": false
}
```

See [Disable artifacts](https://code.claude.com/docs/en/artifacts#disable-artifacts).
