---
name: compactify
description: Compactify a function or code block while improving readability, by trying multiple forms and verifying each preserves behavior. Use when the user says make this more elegant, simplify, tighten, shorten, compactify, clean up, or make more readable.
allowed-tools: Read, Edit, Bash, Grep, Agent
---

# Compactify

Make code shorter AND clearer while preserving behavior. Compaction is a **search over candidate forms**, not a single rewrite. Smaller is only better when it is also clearer — stop when fewer lines start to obscure intent.

## Core loop

1. **Baseline first.** Run the relevant tests BEFORE touching anything. You need a known-green reference to attribute failures to. Note which test asserts the *meaning* (the semantic anchor), not just that it imports.
2. **Generate several candidate forms**, not one. A boolean-equality, a different reduction, an inline, a caller-side change. The first idea is rarely the best.
3. **Apply one candidate, run tests.** Green and clearer → keep. Red → step 4. Not clearer → discard even if green.
4. **On failure, isolate before blaming your edit.** Revert your change and re-run. If it still fails, the failure is pre-existing or latent — your edit exposed it, didn't cause it. Diff against the last known-green commit (`git stash` / compare to HEAD) to find the real source.
5. **Repeat** until you have the smallest form that is still the clearest.
6. **Clean ripple effects.** A removed branch/return can leave dead vars, unused imports, now-impossible type-hint members (e.g. `| int` after the `return 0` is gone). Remove them.
7. **Lint + type-check + full affected suite**, then report.

## Rules that earn their place

- **Verify every candidate by running it. Never trust by reading.** Elegance that changes behavior is a regression, not elegance.
- **Answer correctness questions empirically.** "Is this guard/branch/check needed?" → delete it and run the suite (especially the semantic anchor). Do not argue it from first principles — pandas/numpy/linopy edge behavior defeats reasoning.
- **Know what each intermediate IS** — shape, dtype, index identity, truthiness. Most compaction breaks are shape/alignment/truthiness, not logic: 2D mask on a 1D index, `bool(Index)` is ambiguous, numpy boolean indexing is positional.
- **Look outside the function's scope.** The cleanest win is sometimes in the caller, or in deleting a concept the function only exists to work around. Don't anchor on the lines you were handed.
- **Prefer one-line statements; extract rather than wrap.** A statement that fits on one line reads as a single thought. When an expression would sprawl into a multi-line bracketed pile of nested calls, don't wrap it across lines — lift the intermediates into named locals, each its own one-liner. More assignment lines is the right trade here: line *count* goes up in service of clarity, and every line stays a complete, debuggable thought. This is the opposite failure mode from the anti-pattern below — collapsing logic into one dense line. Compaction targets needless line *spread*, not readable line count. Only extract when the name adds meaning; trivial args stay inline.
- **Name the invariant that makes the compact form correct.** If a one-liner only works because of an ordering/alignment guarantee established elsewhere, that invariant is now load-bearing — keep it, and note it if non-obvious so a later refactor doesn't silently break it.
- **Preserve the public contract** — signature, return types, raised exceptions, side effects — unless the user asked to change it.

## Delegating verification

Compaction generates many small, isolated, answerable questions — "does linopy's empty `.sel` corrupt the expression?", "is `keep` ever empty in this network?", "what shape/dtype is this intermediate?", "is form A truly equivalent to form B across edge cases?". Each is a self-contained experiment whose *conclusion* you need but whose *exploration* would clutter your context.

Delegate these to a subagent (`Agent`): give it the precise hypothesis, the file/test to probe, and ask for a yes/no verdict plus the evidence (the failing line, the printed shape, the test result) — not a file dump. Run independent checks concurrently in one message.

- Use it for **verifying an assumption** before you build a candidate on it, or **confirming a candidate is safe** when the check needs a scratch script or a long suite run.
- Keep the **decision** yourself: the agent returns evidence; you judge whether the form is clearer and keep/discard it. Never let a delegated "looks fine" substitute for the semantic-anchor test passing in your own run.
- For the final green/lint/type gate, run it yourself — that's the record you report.

## Anti-patterns

- Collapsing lines until each is dense and unreadable — that's obfuscation, not compaction.
- Stopping at the first green rewrite without trying alternatives.
- Reasoning "this should be equivalent" instead of running it.
- Attributing a test failure to your edit without isolating against the baseline.

## What "done" looks like

Smallest form that is still the clearest; full affected test suite green (including the semantic anchor); lint + types clean; ripple cleanup done. Report the variants you tried and why the chosen one won.
