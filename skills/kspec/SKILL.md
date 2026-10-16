---
name: kspec
description: Create or update `agents/spec.md` through an interactive product-specification process. Use when defining, changing, or recording product behavior, not merely to read the specification.
argument-hint: "[behavior to specify, or blank to create/review the specification]"
---

## Objective

Define the project's observable behavior in `agents/spec.md`. Resolve open product decisions with the user before writing. Keep implementation planning out of the specification.

## Establish the work

1. Read `<specification_work> $ARGUMENTS </specification_work>` and locate the repository root. If no argument is supplied, read the existing specification to identify gaps or begin defining the product if none exists.
2. Read `AGENTS.md` and `agents/spec.md` when they exist. For a new specification, also read the README and the relevant user-facing documentation, examples, and tests.
3. Separate behavior the user has decided from behavior that remains unsettled. Existing code is evidence of current behavior; do not turn accidental implementation details into requirements.

## Discuss

4. Accept decisions the user has already made. Do not ask for confirmation or ask questions the repository already answers.
5. Resolve each open product decision with the user, one focused question at a time, and wait for the answer. Give the options, their trade-offs, and a recommendation. Use relevant examples from comparable software and include a small example when the choice affects an interface. Speak clearly and simply.
6. For a new product, begin with what the software is for and how people or other systems use it. Let the user's answers determine what needs specifying. Do not infer a product or roadmap from the template.
7. Record decisions as the discussion proceeds. Wait until the scope and decisions are settled before writing `agents/spec.md`. If the user ends the discussion early and asks to save it, write only the settled behavior and identify the unresolved questions.

## Write

8. Update `agents/spec.md` once after the discussion, carrying every settled decision into that write. For a new file, read this skill's `assets/_template.md` and use the sections that apply. Create `agents/` if needed. Use the project name in the title when known; otherwise use `Specification`.
9. Write behavior a reader can check against the running product. Cover inputs, outputs, state changes, errors, and ordering where relevant. Use small examples when prose alone is ambiguous. Record an intentional omission only when it is a product decision, not simply unfinished work.
10. Keep implementation structure, algorithms, dependencies, work ordering, and task status out of the specification. Those belong in architecture, code, or the backlog. Give each fact one home and refer to it elsewhere rather than repeating it.
11. Preserve unrelated existing requirements. Do not present undecided behavior as settled. Remove unused template headings and placeholder text. The specification is authoritative for the behavior it explicitly defines.
12. Give the final response and stop.

## Final response

Summarize what was specified and the important decisions, including their reasons when useful. Write plainly and leave out the steps you took. Do not include a `Next:` section or suggest a follow-up command.

```markdown
Two to four sentences describing the behavior defined or changed.

**Specification:** `agents/spec.md`

**Decisions:**

- An important product decision and why it was made.
```

Omit Decisions if there are no important decisions to call out. If questions remain unresolved, name them briefly without presenting them as requirements.
