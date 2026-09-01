# Shared Review Rubric

Shared by `review-full`, `review-full-branch`, `review-diff`, `review-diff-branch`. Each of those skills sets the **scope** (which git command, full files vs. diff) and then applies everything below. Read this file in full before spawning reviewers.

Guiding principle: **signal over noise**. A good review surfaces a handful of issues a competent engineer would actually fix, not a flood of suggestions. If in doubt, drop it.

## 1. Ignore filter

Skip these — never report issues in them:
- Lock files (`*.lock`, `package-lock.json`, `poetry.lock`, `uv.lock`, `Cargo.lock`, `go.sum`).
- Minified / bundled / vendored assets (`*.min.js`, `*.min.css`, `dist/`, `build/`, `vendor/`).
- Source maps (`*.map`), snapshots (`*.snap`), compiled artifacts (`__pycache__`, `*.pyc`).
- Any file containing a `@generated` / `// Code generated` marker in its first ~5 lines.

**Exception:** database migration files are reviewed even when generated.

## 2. Risk tiering — how many reviewers to run

Scale the reviewer fleet to the size and sensitivity of the change. Count changed lines across source files (after the ignore filter).

| Tier | Size | Reviewers to run |
|---|---|---|
| Trivial | ≤10 changed lines | **Correctness & Security** only |
| Lite | ≤100 changed lines | Correctness & Security + Code Quality |
| Full | >100 lines, or 10+ files | all four dimensions |

**Override:** if any changed file is security-sensitive — auth, crypto, session/token handling, SQL or query building, deserialization, subprocess/shell, file path handling, network input parsing — run the **Full** fleet regardless of size.

Always run the verification/coordinator pass (section 6), even on Trivial.

## 3. Reviewer dimensions (and what NOT to flag)

Spawn reviewers as parallel `reviewer` agents. The negative lists matter as much as the positive ones — telling the reviewer what to ignore is what keeps the review high-signal.

**1. Correctness & Security** *(always runs)*
- Look for: logic bugs, off-by-one, wrong types passed, broken invariants, unhandled error paths that can actually occur, resource leaks; injection (SQL/command/path), missing authz/authn checks, secrets in code, unsafe deserialization, unvalidated external input.
- Do NOT flag: theoretical risks requiring unlikely preconditions; defense-in-depth when the primary defense is already adequate; "add error handling" to code that already handles the error; speculative concurrency bugs you cannot trace to a concrete interleaving.

**2. Code Quality**
- Look for: DRY violations (a *block* of logic duplicated that should become a shared helper), KISS violations, missing early returns, dead code, unused imports, genuinely confusing names.
- Do NOT flag: style/formatting a linter or formatter owns; short statements repeated a couple of times (extraction not worth it); requests to add comments; abstraction for its own sake.

**3. Type & API**
- Look for: missing/incomplete type hints on public surfaces, inconsistent annotations, backward-incompatible signature/contract changes, misleading names.
- Do NOT flag: missing docstrings on private/trivial helpers; annotations a type checker already infers; nitpicks on internal-only helpers.

**4. Test Coverage**
- Look for: changed behavior with no test, uncovered error/edge cases that matter, brittle or non-deterministic tests, assertions that don't actually assert the behavior.
- Do NOT flag: missing tests for trivial pass-through/glue code; "add a test" without naming the specific uncovered behavior; coverage of code a test already exercises indirectly.

## 4. Evidence requirement (false-positive filter)

The changed lines alone are not enough context to judge most issues. Every reported issue MUST include:
- **Claim**: one sentence, with `file:line`.
- **Evidence FOR**: the exact offending line(s), quoted.
- **Evidence AGAINST being a false positive**: proof the reviewer checked beyond the changed lines when relevant — quoted call sites, type definitions, existing tests, or `git grep` results. For "dead code" / "unused" claims, the reviewer MUST have grepped for usages and report what they found. For "missing type" / "wrong type" claims, the reviewer MUST have read the referenced symbol's definition.
- **If the reviewer cannot produce the AGAINST evidence, the issue is dropped — not reported as low-confidence.**

## 5. Classification

Classify each surviving issue as `must-fix` or `nice-to-have` (no wider severity scale — only report what you'd actually fix), and tag each as:
- `[task-related]` — in files changed by this task, related to its purpose.
- `[drive-by]` — pre-existing problem in untouched code, or unrelated to the task.

Format: `| Issue | file.ts:123 | must-fix/nice-to-have | [task-related]/[drive-by] |`

## 6. Coordinator (verification + verdict)

After the reviewers return, run ONE more `reviewer` agent as coordinator. Give it the consolidated findings and instruct it to:
1. **Deduplicate** issues flagged by more than one reviewer; **re-categorize** any misfiled finding.
2. For each issue, **independently reproduce the evidence** (read the file, grep for usages, check the test). Discard any issue it cannot reproduce, or where wider context contradicts the claim.
3. Emit an overall **verdict** on this rubric:
   - `request-changes` — at least one surviving `must-fix`.
   - `approve-with-comments` — only `nice-to-have` issues survive (a lone `nice-to-have` never blocks).
   - `approve` — nothing survives.

Address all surviving `must-fix` `[task-related]` issues. Defer `[drive-by]` and `nice-to-have` issues (and skip any that would introduce over-engineering); document them as deferred.

## 7. Honest limitations

AI review is weak at: architectural/design intent, cross-system impact (e.g. an API contract change affecting downstream consumers), and subtle concurrency/race conditions. Where a concern falls in these areas, the coordinator should surface it as **"needs human judgment"** with its reasoning, rather than asserting it as a confirmed `must-fix`.
