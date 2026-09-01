# claude-config

My personal configuration for [Claude Code](https://claude.com/claude-code), Anthropic's terminal coding agent. This repository holds the settings, the writing style, the automation hooks, and a library of reusable skills that shape how the agent works for me.

You can copy any part of it into your own `~/.claude/` directory.

## Recommended models

- **Opus 4.8** for all day-to-day work and for implementation. It is the strongest general model here and the default in `settings.json`.
- **Fable 5** for planning. Use it when you design an approach before writing code, for example with the `plan-prepare` and `plan-orchestrate` skills.

In short: plan with Fable 5, then build and do everything else with Opus 4.8. Use Sonnet 5 for sub-agentic tasks and for delegated work with clear scope.

## Core concepts

Claude Code reads a few kinds of files from `~/.claude/`. Each one controls a different part of the agent's behavior.

### 1. Global instructions (`CLAUDE.md`)

House rules that apply to every project. Mine cover Python style (DRY, KISS, fail fast, typing, no filler comments), git habits, and how to delegate work to sub-agents.

### 2. Output style (`output-styles/standard.md`)

An output style (a reusable preset for the agent's voice) defines *how* the agent talks, not *what* it does. My `Standard` style enforces:

- The answer first, in one or two sentences, then the reasoning.
- Plain language following ASD-STE100 (Simplified Technical English), with every jargon term glossed.
- Reference codes like `[F1]` so findings can be cited later in the chat.
- A closing one-line takeaway plus numbered next steps.

### 3. Settings (`settings.json`)

The main control file. It sets the default model, the permission allow and deny lists (which shell commands run without a prompt), enabled plugins, the status line, hooks, and preferences like theme and voice input.

### 4. Hooks (`hooks/`)

Small scripts the agent runs automatically at set moments. `context-warn.sh` fires when the conversation grows past a token threshold and reminds me to compact or offload to a sub-agent.

### 5. Skills (`skills/`)

The largest part of this repo. A skill is a packaged instruction set for one kind of task. The agent loads a skill when the task matches, or I trigger it by name with a slash, for example `/git-commit`. Every name carries a group prefix (`plan-`, `review-`, `git-`, `code-`, `doc-`), so related skills sort together. See the full list below.

### 6. Status line (`statusline-command.sh`)

A script that renders the bar at the bottom of the terminal: current context usage, git branch, and task metrics.

## Skills

Grouped by purpose.

### Planning and delegation (`plan-`, `sub-`)

| Skill | What it does |
| --- | --- |
| `plan-prepare` | Write a concrete implementation plan from a discussed request. |
| `plan-implement` | Materialize a plan into working code. |
| `plan-orchestrate` | Turn a plan into a sub-agent execution strategy. |
| `plan-handoff` | Write a handoff prompt to resume work in a fresh session. |
| `sub-run`, `sub-this`, `sub-review` | Delegate a task, or a plan review, to a sub-agent. |

### Code review (`review-`)

| Skill | What it does |
| --- | --- |
| `review-diff`, `review-diff-branch` | Parallel reviewers over the current diff or the branch diff. |
| `review-full`, `review-full-branch` | Deeper review that reads full file context, not just the diff. |
| `review-edits` | Review uncommitted edits I made by hand. |

### Git, PRs, issues, and CI (`git-`, `pr-`, `issue-`, `ci-`)

| Skill | What it does |
| --- | --- |
| `git-commit`, `git-push` | Write a compact commit message and optionally push. |
| `git-history`, `git-worktree` | Investigate history, or work on branches in parallel. |
| `pr-raise`, `pr-prime` | Open a pull request, or read an existing one for context. |
| `issue-draft`, `issue-raise`, `issue-solve` | Draft issues locally, file one on GitHub, or drive one to a fix. |
| `ci-fix`, `ci-monitor` | Read the CI status and fix failing checks. |

### Code quality (`code-`)

| Skill | What it does |
| --- | --- |
| `code-fix-bug` | Fix a reported bug in a production-ready way. |
| `code-compactify` | Tighten a function while keeping behavior and readability. |
| `code-test-refactor` | Make tests concise, parametrized, and fixture-reusing. |
| `code-todos` | Resolve TODO comments in the current diff. |
| `code-batch-constraints` | Batch linopy constraint additions (energy-modelling specific). |

### Documentation and meta (`doc-`, `meta-`)

| Skill | What it does |
| --- | --- |
| `doc-release-notes` | Add release notes for the proposed changes. |
| `doc-slides` | Build slide decks from Markdown with Marp. |
| `meta-skill` | Create new skills for this repo. |

## Layout

```
CLAUDE.md              Global house rules for every project
settings.json          Main config: model, permissions, plugins, hooks
output-styles/         Reusable voice presets (Standard)
hooks/                 Scripts the agent runs on events
skills/                Reusable task instruction sets
statusline-command.sh  The terminal status bar
teams/                 Multi-agent team configuration
policy-limits.json     Remote-control and web-setup restrictions
```

Machine-specific and runtime files (credentials, transcripts, sessions, caches) are excluded through `.gitignore`.
