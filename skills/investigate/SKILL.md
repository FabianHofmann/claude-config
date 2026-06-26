---
name: investigate
description: Parallel Codebase Investigation. Spawn 4 exploration agents to investigate a topic from different angles. Use when deeply investigating a feature, module, or concept.
---

# Parallel Codebase Investigation

Spawn 4 exploration agents **in a single message** to investigate the user's specified topic from different angles.

---

## Agents to Spawn (ALL IN ONE MESSAGE)

### Agent 1: Structure Scout (`Explore`, model: haiku)
```
Map the high-level architecture related to: <topic>

Find:
- Entry points and main modules
- Core files handling this functionality
- Data flow (input → processing → output)

Return:
- File paths with 1-sentence descriptions
- Architectural pattern used (MVC, hexagonal, etc.)

Keep output under 200 words. Prioritize relevance over completeness.
```

### Agent 2: History Miner (`general-purpose`, model: haiku)
```
Investigate git history for: <topic>

Run these commands and analyze:
- `git log --oneline -30 --all -S '<topic>'` (when code was added/changed)
- `git log --oneline -20 --all -- '*<topic>*'` (file history)
- `git shortlog -sn --all -- <relevant_paths>` (who maintains it)

Return:
- When feature was introduced (commit + date)
- Primary maintainer(s)
- Recent significant changes (last 3)
- Any related issues/PRs mentioned in commits

Keep output under 200 words.
```

### Agent 3: Test Cartographer (`Explore`, model: haiku)
```
Find all tests related to: <topic>

Identify:
- Test file locations (exact paths)
- Key test function/method names
- Fixtures, mocks, or factories used
- Test coverage gaps (untested code paths if obvious)

Return as compact list with file:line references.
Under 150 words.
```

### Agent 4: Dependency Tracer (`Explore`, model: haiku)
```
Trace dependencies for: <topic>

Find:
- What this code imports/depends on (internal and external)
- What other code imports/depends on this
- Shared types, interfaces, or protocols involved

Use grep for import statements. Limit to 2 levels deep.
Return as a dependency summary.
Under 150 words.
```

---

## Synthesis (after all agents return)

Combine findings into a single actionable summary:

### Quick Facts
- **Location**: [primary file/module path]
- **Maintainer**: [name from git history]
- **Last Changed**: [date and context]
- **Test Coverage**: [location and assessment]
- **Dependencies**: [key internal/external deps]

### Key Files (ranked by relevance)
| File | Role | Priority |
|------|------|----------|
| path | what it does | read first / modify / reference only |

### Entry Point
[The single best file to start reading/modifying, with reasoning]

### Suggested Approach
1. [Concrete first step]
2. [Second step]
3. [Third step]

---

## Save Context
Write synthesis to `.claude-context/investigation-<topic>.md` for future reference.
