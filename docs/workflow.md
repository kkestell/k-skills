# An Agentic Development Workflow

### Framing

> The ability to simplify means to eliminate the unnecessary so that the necessary may speak.<br>— Hans Hofmann

This workflow is for developers who want to keep working the way they always have, only faster. It works through one task at a time. No swarms of autonomous agents, no worktrees. It assumes the developer roughly knows what they want to build, makes the architectural decisions, and reviews the code. The goal isn't to replace developers with agents.

This may be simpler than you're expecting. It's just you, an agent harness, your code, a couple files, and three agent skills.

Don't forget:

- This stuff changes _fast_. This is my workflow today. It probably won't be my workflow tomorrow. Stay nimble.
- Do what works for you, your team, and your project.
- Don't believe the hype. Nobody has this figured out yet. Use agents to write code, read that code, and form your own opinions.

### Overview

The whole system is built on a simple one-to-one correspondence: **one task, one plan, one session to implement the plan, one review, and one commit.** Each task from the backlog goes through the same loop: the agent writes a plan you can steer, implements it, and reviews the result, asking you about anything that needs a decision. Then everything is committed together and the task is checked off.

![The workflow: spec.md and todo.md feed Plan, Work, Review, and Commit, then the task is checked off](workflow.svg)

### Project Layout

The workflow is deliberately small. A complicated process takes mental effort just to keep straight: what step comes next, which files exist at this point, etc. That effort is better spent on the work. The whole workflow needs only three files:

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

### Agent Instructions (`AGENTS.md`)

> The more you tighten your grip, Tarkin, the more star systems will slip through your fingers.<br>— Princess Leia Organa

Keep `AGENTS.md` short. A model has limited attention, and you want it thinking about your code, not your workflow.

Most rules will be workarounds for quirks in whatever model you happen to be using. The next model may not have those quirks, and then the rules just tell it to do what it would have done anyway, while still taking up its attention. With many rules, it's hard to tell which rules are still doing anything. So start with very few. Do real work, look critically at the output, and add rules sparingly.

Here's an example:

```markdown
# Project

Describe your project in one sentence.

## Commands

- `npm run lint` runs every check.
- ...

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
```

The documentation rules limit documentation to what the code can't say for itself. Left alone, coding agents write a lot of documentation, and most of it just restates the code in prose. Those files grow fast, use up output tokens, and have to be updated every time the code changes. Deleting them doesn't make the agent's work any worse. It can read the code to find out what the code does, and unlike the docs, the code is never out of date.

### The Spec (`agents/spec.md`)

The spec comes first, written by hand or with the agent. It's the single source of truth for external, user-facing behavior, integrations with external systems, and invariants. It's like a programming language or network protocol specification: it describes observable behavior, not the internal implementation.

The spec doesn't have to be complete upfront. In fact, it's usually better if it isn't. You won't always have line of sight on everything initially, and you'll often need to experiment and build a bit before you know the full shape of what you're making.

### The Backlog (`agents/todo.md`)

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

Tasks are checked off as they're done, but milestones don't have checkboxes. When a milestone is finished, it's deleted from `todo.md`. Otherwise the file keeps growing, and the plans, work logs, reviews, and commit history are a much better record of what got done anyway. Tasks keep their checkboxes because they don't mean much outside their milestone, and a milestone usually takes many sessions, sometimes several days, to finish. The checkboxes show how far along the current one is.

### The Architecture (`agents/architecture.md`, optional)

`architecture.md` documents the project's implementation constraints and the reasoning behind key design decisions. It covers dependency boundaries, ownership of shared state and resources, and how work is split across threads or processes.

This file can easily accumulate cruft, so keep it focused on high-level architecture. Do not let it become a running commentary on the code. Most code changes shouldn't touch it; update it only when the architecture changes. Include it only when the project needs these rules and decisions documented.

### Running a Task

#### 1. Plan ([`kplan/SKILL.md`](https://github.com/kkestell/skills/blob/main/kplan/SKILL.md))

```
/kplan the next task in agents/todo.md
```

The plan skill takes the next task in `todo.md`. The agent explores the codebase, works through any open design decisions with you, and writes an implementation plan to `agents/plans/`.

Planning upfront forces the agent to confront edge cases before writing code, lets you use a cheaper, faster model for the implementation, and lets you steer the design before bad code is written.

#### 2. Work ([`kwork/SKILL.md`](https://github.com/kkestell/skills/blob/main/kwork/SKILL.md))

Once the plan looks right, the work skill takes over. The agent implements the plan, runs the checks, and writes a work log to `agents/work/` recording how the change was verified, where it departed from the plan, and any surprises it ran into.

#### 3. Review ([`kreview/SKILL.md`](https://github.com/kkestell/skills/blob/main/kreview/SKILL.md))

After the implementation is done, the review skill checks it. The agent reviews the changes against the plan, fixes trivial issues directly, and asks you to decide on anything non-trivial. It writes the review to `agents/reviews/` and commits the plan, code changes, work log, and review together.

### Models and harnesses

The skills ([`skills`](https://github.com/kkestell/skills)) are written to work in more than one agent harness. They work with Claude Code, Codex, and OpenCode, so you can pick the model for each step. It's worth running the review with a different model from the one that wrote the code.

### Sessions

The spec, to-do, plan, and work can all happen in a single session, as long as you keep an eye on the context window. Other times it makes sense to split things up: the spec and to-do in one session, then plan, work, and review each in a fresh session.

The trade-off is that the agent has to reorient itself at the start of every fresh session. Prefix caching makes long sessions much, much cheaper than they look.

### Examples

Here are a few projects built with this workflow. Their repositories show what the generated plans, work logs, reviews, and commit histories look like in practice:

- **[Ox](https://github.com/kkestell/ox)**: An ACP-native coding agent in Go, with an ACP server and a terminal UI.
- **[Willow](https://github.com/kkestell/willow)**: A small, statically typed language with Python-like syntax that compiles to Lua and runs on LuaJIT.

### Claude Code Tips and Tricks

#### No Free Advertising

Disable Claude's attribution in commits and pull requests:

```json
{
  "includeCoAuthoredBy": false
}
```

See the [attribution settings](https://code.claude.com/docs/en/settings-reference#includecoauthoredby).

#### Spinner Verbs

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

#### Disable Artifacts

Turn off Claude Code's Artifact tool:

```json
{
  "enableArtifact": false
}
```

See [Disable artifacts](https://code.claude.com/docs/en/artifacts#disable-artifacts).
