---
name: orchestrate-plan
description: "Turn an implementation plan into an orchestration plan: how Claude Code should drive it with subagents, teams, and skills. Use when the user has a plan (file or description) and asks for an orchestration plan, execution strategy, subagent breakdown, or how to drive a multi-phase implementation."
---

# Orchestrate Plan: Implementation → Orchestration Strategy

Read an implementation plan and produce a *companion* orchestration plan describing how the main Claude Code conversation should drive it end-to-end using subagents, teams, parallel fan-outs, and existing skills.

**Input**: a path to an implementation plan file, OR a plan that only exists in the conversation.

**Flow**:
- **Plan file already exists** → read it, append the orchestration section directly (no plan mode needed).
- **Plan only in conversation** → call `EnterPlanMode`. Inside plan mode, develop the full plan *with the orchestration section already included* and present it for the user's approval via `ExitPlanMode`. After the user approves, write the approved plan + orchestration to a markdown file (ask for the path/filename if not obvious from context). Plan mode is read-only, so the file write happens only after approval — that's intentional.

**Output**: a single markdown file containing BOTH the plan and the orchestration strategy, with a clear separator (`---` and `# Orchestration strategy` heading). If the plan was already in its own file, append the orchestration section to it rather than creating a sibling file.

**Required header**: the file MUST start with the last commit hash for reference, captured via `git rev-parse HEAD` (and a short `git log -1 --oneline` line for human context). This anchors the plan to a known baseline.

Reference: `/home/fabian/vres/py/pypsa/dev-scripts/storage-unit-to-store-orchestration.md`.

---

## Core principle — do NOT default to fan-out

The instinct is to parallelise everything. That's usually wrong. Fan out only where files are **genuinely independent** (no shared masks, sign conventions, predicates, or interlocking types). Tightly-coupled reasoning belongs in a *single* agent with a long, explicit prompt — three agents independently inventing slightly different abstractions is worse than one slower coherent pass.

Apply this lens to every phase before recommending parallelism.

---

## Steps

1. **Locate or develop the plan.**
   - If the user provided a file path, read it in full. Capture the current commit hash (`git rev-parse HEAD`) and add a `**Baseline commit:**` line at the top.
   - If the plan only exists in conversation, enter plan mode (`EnterPlanMode`). Develop the full plan + orchestration section together inside plan mode and present them for approval via `ExitPlanMode`. Only after approval, write the file to disk with the baseline-commit header.
   Note when reading/developing: file lists per phase, dependencies between files, sign/convention/predicate threads, test surface, deprecation/docs items.
2. **Extract the dependency shape.** Which phases hard-block which? Which can run alongside? Draw it as an ASCII graph.
3. **Classify each phase** as one of:
   - *Single subagent, sequential* — interlocking design, shared invariants, or files always read together.
   - *Fan-out, parallel* — file-isolated, no shared invariants, mergeable independently.
   - *Fork (single agent, isolated context)* — noisy exploration or baseline-capture whose transcript should not pollute coordinator context.
4. **Pick skills** where they fit (don't invent new ones): `fan-out`, `sub`, `subs`, `tm`, `implement-feature`, `investigate`, `abs-review-branch` (prefer for review gates — full-file context reduces false positives), `diff-review-branch` (only for large mechanical/rename changes where reading files in full is wasteful), `raise-pr`, `commit`, `push`, `ci-monitor`, `git-worktree`. Prefer a plain `general-purpose` Agent when a skill would be overkill — say so explicitly.
5. **Place review gates** between phases (cheap insurance — 3 parallel reviewers cost less than one fix cycle later).
6. **Decide what stays in coordinator context** vs what lives only in subagent transcripts.
7. **Write the orchestration section** into the same plan file, separated by `---` followed by the `# Orchestration strategy` heading, using the template below.
8. **State the main tradeoff** at the end — the user should see the cost of the recommended sequencing vs the alternative (usually: coherence vs wall-clock).

---

## Template

The final file looks like this — plan above, orchestration below, separated by `---`:

```markdown
# <Plan title>

**Baseline commit:** `<short-sha>` — <subject line from `git log -1 --oneline`>

<full implementation plan content — phases, file lists, rationale, etc.>

---

# Orchestration strategy

Follow this orchestration strategy to implement the plan above. Only diverge from this strategy if there is a compelling reason to do so.

## Dependency shape

\`\`\`
A (<role>)  →  B (<role>)  →  C (<role>)  →  D (<role>)
                    ↓
                 <parallel work>
\`\`\`

Hard sequencing: <one sentence naming the concrete dependency — e.g. "B reads columns added in A; C's migration depends on B's new variables">.

## Phase-by-phase orchestration

### Phase 0 — <Baseline / exploration> (fork, ~N min)

<Only if useful: a single fork captures golden snapshots / explores. Forking keeps tool noise out of main context. State the artifact (fixture file, summary doc).>

### Phase A — <name> (single subagent, sequential)

<Why one agent: these files are read together, share invariants X/Y. Exit criterion: tests <names> pass + baseline holds.>

### Phase B — <name> (single subagent, NOT fanned out)

<Spell out the interlocking concern — masks/signs/predicate that threads through every file. A fan-out here means N agents independently inventing slightly different <thing>. One agent with a long, explicit prompt listing every line reference from the plan. Commit incrementally so a failure at step N doesn't lose 1..N-1. Note whether `implement-feature` is overkill vs a plain `general-purpose` agent.>

### Phase C — Fan-out (parallel subagents)

<Why this one IS independent. Use the `fan-out` skill or parallel Agent calls in one message:>

- **C.1**: <file/scope>
- **C.2**: <file/scope>
- **C.3**: <file/scope or "fold into C.1 if scope shrinks">

The coordinator collects results and runs <gate command> as the merge gate.

### Phase D — <name> (parallel / sequential — pick one and justify)

- **D.1**: <scope>
- **D.2**: <scope>

## Review gates

After each phase, run `abs-review-branch` (default — full-file context reduces false positives). Use `diff-review-branch` only for large mechanical changes (renames, sweeping refactors) where reading every file in full is wasteful. Cheap insurance either way.

## What stays in the coordinator's context

The coordinator keeps:
- the plan file
- <baseline fixture / key artifact>
- the current phase's diff summary

Everything else — exploration output, raw test logs, intermediate refactors — lives in subagent transcripts.

## Concrete kickoff sequence

1. Branch off `<base>` to `<feat/branch-name>`.
2. <Fork / baseline> → commit fixture.
3. Subagent: Phase A → commit → review gate.
4. Subagent: Phase B → commit-per-step → review gate.
5. Parallel agents: Phase C → merge → review gate.
6. Parallel agents: Phase D → merge → full-suite + `mypy` + `pre-commit`.
7. `raise-pr` skill.

## Main tradeoff

<One paragraph: the recommended sequencing trades X for Y. Name the alternative (usually more fan-out) and why its wall-clock gain is eaten by a merge-conflict / convention-drift cleanup.>
```

---

## Heuristics for the classification step

| Signal in the plan | Phase type |
|---|---|
| "masks/signs/predicate must agree across files" | single agent |
| "these three files are read together every time" | single agent |
| "migration helper", "release notes", "deprecation log" | fan-out |
| "audit X across the codebase", "verification + minor edits" | fan-out or fork |
| "capture baseline / golden snapshot" | fork |
| "broad codebase exploration > 3 queries" | fork via `investigate` or `Explore` agent |
| < 3 files total in a phase | no subagent — edit directly |

## When NOT to use this skill

- The plan describes a single small change (just implement it).
- The plan has no phases / no obvious dependency structure (push back: ask the user to firm the plan first).
- The user wants the implementation itself, not a strategy — use `implement-feature` instead.
