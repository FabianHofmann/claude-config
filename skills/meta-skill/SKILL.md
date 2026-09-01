---
name: meta-skill
description: Create Claude Code skills. Use when the user wants to add a skill, create a skill, write a skill, or document a workflow for Claude to use automatically.
---

# Creating Claude Code Skills

Skills give Claude specialized knowledge that activates when relevant to the user's request.

## Directory Structure

```
~/.claude/skills/<skill-name>/
├── SKILL.md              # Required
├── reference.md          # Optional - detailed docs
└── scripts/              # Optional - utility scripts
```

Personal skills go in `~/.claude/skills/`, project skills in `.claude/skills/`.

## SKILL.md Format

```yaml
---
name: skill-name
description: What the skill does. Use when [trigger conditions].
---

# Skill Title

## Instructions
Step-by-step guidance for Claude.

## Examples
Concrete usage examples.
```

## Required Frontmatter

| Field | Description |
|-------|-------------|
| `name` | Lowercase, hyphens allowed, must match directory name |
| `description` | What it does + when to use it (trigger keywords) |

## Optional Frontmatter

| Field | Description |
|-------|-------------|
| `allowed-tools` | Tools Claude can use without asking (e.g., `Read, Grep`) |
| `model` | Specific Claude model to use |
| `context: fork` | Run in isolated sub-agent context |
| `user-invocable: false` | Hide from slash command menu |

## Description Best Practices

Include trigger keywords users would say:

```yaml
# Bad
description: Helps with documents

# Good
description: Extract text from PDFs, fill forms. Use when working with PDF files or document extraction.
```

## Example Skill

```
~/.claude/skills/commit-helper/SKILL.md
```

```yaml
---
name: commit-helper
description: Generate commit messages from diffs. Use when writing commits or reviewing staged changes.
---

# Commit Message Helper

## Instructions
1. Run `git diff --staged`
2. Suggest message with summary under 50 chars
3. Use present tense, explain what and why
```
