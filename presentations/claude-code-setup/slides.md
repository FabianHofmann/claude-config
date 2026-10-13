---
marp: true
theme: dispatch
paginate: true
size: 16:9
footer: 'Claude Code: lessons learned'
---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _footer: '' -->

<div class="legend"><span>Why</span><span>Anatomy</span><span>Context</span><span>Tracking</span><span>Quality</span><span>Adopt</span></div>

# Keeping LLMs focused, traceable and efficient

<p class="sub">Lessons learned on how to setup Claude Code for day-to-day work</p>

<p class="who">Fabian Hofmann, Open Energy Transition</p>

<!--
Fifteen minutes of lessons learned from daily work with Claude Code, and what we recommend as a result. Every recommendation maps to plain files in ~/.claude that you can copy.
The bar at the top of each slide is the talk timeline: grey is ahead, amber is where we are.
-->

---

<!-- class: p1 -->
<!-- header: 'Why' -->

## The agent scales. Three things do not.

<p class="lede">Agents now run for an hour, read dozens of files and write hundreds of lines. The human job moves from writing code to orchestrating and checking it.</p>

<div class="limits">
<div><b>Context</b>what the model can hold</div>
<div><b>Attention</b>what you can follow</div>
<div><b>Trust</b>what you can merge without reading</div>
</div>

> Lesson: the limits are on the model's memory and on the human, not on the model's speed.

<!--
The agent got much faster and more capable. Three things did not grow with it: the context window, your attention and your trust in the output.
The rest of the talk is about these three limits, one slide each, then what helps.
-->

---

<!-- header: 'Why: context' -->

## Limit 1: the context window

<p class="big">~200k <small>tokens</small></p>

- decreased quality
- slower
- higher costs
- every turn sends the whole history again

> Lesson: every file the agent reads is paid for again on every later turn.

<!--
Think of the context like the memory budget of a solve. Everything the agent read stays in the window and is paid for again each turn.
Past roughly 200k tokens, answers get worse, replies get slower and bills go up. Each turn re-sends everything, so a file dump early in the session costs on every turn after it.
-->

---

<!-- header: 'Why: attention' -->

## Limit 2: your attention

- The agent produces a lot of text and a lot of options
- After an hour you have ten open threads and three half-made decisions
- A rewind or a compaction silently drops some of them
- Permission prompts break the flow, and approving by reflex is unsafe
- Two weeks later: *why did this line change?*

> Lesson: the bottleneck is human attention, not model speed.

<!--
Quick show of hands: who had a session go off track after a compaction?
The agent is fast; the human is not. Long answers with many options make it easy to lose the thread.
Worse, rewinds and context compaction can drop open items without anyone noticing. Weeks later, nobody can explain why a change was made.
-->

---

<!-- header: 'Why: trust' -->

## Limit 3: plausible is not good

<div class="cols w">
<div>

LLM code carries habits:

- defensive `try/except` that hides errors
- `hasattr` / `getattr` probing
- filler comments that restate the code
- long, repetitive tests
- mocks everywhere

</div>
<div>

```python
try:
    n.optimize()
except Exception:
    # Optimization failed, continue
    pass
if hasattr(n, "buses"):
    ...
```

</div>
</div>

> Lesson: self-review is weak. The writer rarely finds its own mistakes.

<!--
The code looks fine at first glance. But it has habits that hurt in a modelling code base: swallowed solver errors, attribute probing, comments that say nothing.
And if you ask the same agent to review its own work, it mostly agrees with itself.
-->

---

<!-- header: 'Why: overview' -->

## Three limits, three answers

<div class="limits tall">
<div><b>Context</b><p>Make the budget visible, orchestrate sub-agents, write the bulk to files</p><p><code>context-warn.sh</code> <code>sub-*</code> <code>plan-*</code></p></div>
<div><b>Attention</b><p>Skimmable output, a ledger, traceable outcomes, fewer prompts</p><p><code>standard.md</code> <code>ledger.py</code> <code>settings.json</code></p></div>
<div><b>Trust</b><p>Rules for the writer, a separate reviewer</p><p><code>CLAUDE.md</code> <code>review-*</code> <code>implement-review-revise</code></p></div>
</div>

<!--
This is the map for the rest of the talk. Each recommendation answers one limit, and each lives in a plain file you can copy.
-->

---

<!-- class: p2 -->
<!-- header: 'Anatomy' -->

## Where recommendations live: `~/.claude`

<div class="anat">
<div class="box"><b><code>CLAUDE.md</code></b>House rules for every project: Python style, git, delegation</div>
<div class="box"><b><code>output-styles/</code></b>How the agent talks: <code>standard.md</code></div>
<div class="box wide"><b><code>settings.json</code></b>Default model <code>opus</code>, <span class="n">60</span> allow rules for shell commands, plugins, status line, hooks</div>
<div class="box hook"><b><code>hooks/</code></b><code>context-warn.sh</code> on Stop, <code>ledger.py</code> on prompt, stop and compact</div>
<div class="box"><b><code>agents/</code></b><code>implement-review-revise</code> lead agent</div>
<div class="box"><b><code>statusline-command.sh</code></b>Model, branch, context meter, ledger link</div>
<div class="box"><b><code>skills/</code></b><span class="n">36</span> skills, invoked by name, e.g. <code>/git-commit</code></div>
<div class="box wide"><b>Skill groups by prefix</b><code>plan-</code> <code>sub-</code> <code>review-</code> <code>git-</code> <code>pr-</code> <code>issue-</code> <code>ci-</code> <code>code-</code> <code>doc-</code></div>
<div class="box wide"><b>Why it pays off</b>Skills encode team workflows; the allowlist cuts permission prompts</div>
</div>

<!--
Claude Code reads seven kinds of files. CLAUDE.md holds the house rules, the output style sets the voice, settings.json wires everything together.
Hooks are small scripts that run on events. Skills are the bulk: 36 packaged instructions, grouped by prefix so they sort together.
-->

---

<!-- class: p3 -->
<!-- header: 'Context: see it' -->

## Recommendation: make the budget visible

<div class="meter"><span class="g"></span><span class="y"></span><span class="r"></span></div>
<div class="scale"><span>0</span><span>100k: yellow</span><span>150k: red, warning</span></div>

<div class="cols">
<div>

### Warning
- `hooks/context-warn.sh` runs on **Stop**
- Warns at **150k** tokens, then every **25k**
- Suggests `/compact`, `/clear` or a sub-agent
- Status line: green, yellow at 2/3, red at the limit

</div>
<div>

### Model routing
- **Opus**: default, day-to-day work
- **Sonnet**: simple, well-scoped sub-tasks
- **Fable**: hard problems and planning
- Reviews prefer Opus to save tokens

</div>
</div>

<!--
First recommendation: make the budget visible. The status line shows a context meter that turns yellow at two thirds of the threshold and red at 150k.
The Stop hook then posts a warning and repeats it every 25k tokens. The model choice is the second lever: Opus by default, Sonnet for cheap sub-tasks, Fable for hard ones.
-->

---

<!-- header: 'Context: orchestrate' -->

## Recommendation: the main agent decides and orchestrates

<div class="cols w">
<div>

- The main agent plans, dispatches and decides
- Sub-agents read and edit the files; the main agent gets the conclusion
- CLAUDE.md: *for work that you can delegate to sub-agents, do so*
- `sub-run`, `sub-this`: hand a task to a sub-agent
- `sub-implement`: run the full loop on the right

</div>
<div>

<div class="flow" style="flex-direction:column; align-items:stretch">
<div class="st lead">implement-review-revise<small>lead, coordinates only</small></div>
<div class="st">implementer<small>edits, adds tests</small></div>
<div class="st">reviewer<small>evidence, must-fix or nice-to-have</small></div>
<div class="st">reviser<small>fixes task-related issues</small></div>
</div>

<p class="small">Max <strong>2</strong> rounds. Report ≤ <strong>300</strong> words.</p>

</div>
</div>

<!--
Second recommendation: the main agent is an orchestrator. It plans, hands tasks to sub-agents and makes decisions with you. Sub-agents read the files and burn their own context; the main agent only gets the conclusion.
The implement-review-revise lead runs three sub-agents in sequence, at most two rounds, and returns a report of at most 300 words.
-->

---

<!-- header: 'Context: write it down' -->

## Recommendation: put the bulk in files and fresh sessions

- `review-*`: parallel reviewers, fleet scaled by change size
  - ≤ 10 lines: 1 reviewer, ≤ 100 lines: 2, more: all 4, plus a coordinator
- `plan-prepare`: the plan goes to `dev/<topic>/plan.md`, not into the chat
- `plan-handoff`: a ≤ 40-line prompt to continue in a fresh session
- `graft`: a code index; one query replaces many file reads

> Lesson: a fresh session with a good handoff beats a compacted old one.

<!--
Reviews run as parallel agents, and the rubric scales the fleet with the size of the change, so a ten-line fix does not cost four reviewers.
Plans live in files. When a session gets heavy, plan-handoff writes a prompt of at most 40 lines, and a fresh session starts clean.
-->

---

<!-- class: p4 -->
<!-- header: 'Tracking: the voice' -->

## Recommendation: an output style for skimming

<div class="cols">
<div>

- Answer first, then reasons
- ASD-STE100 Simplified Technical English
- ≤ 20 words per sentence, terms glossed
- One sentence to repeat to a colleague
- Numbered next steps as options
- Reference codes you can cite later:
  `F` finding, `C` correction, `I` related issue, `U` unrelated issue, `B` breaking change, `D` decision, `P` PR or issue, `G` goal

</div>
<div>

<pre><code>Yes. The solve fails because bus "DE0 H2"
has no carrier <span class="hl">[F1]</span>. The fix sets it in
add_electrolysers() and adds a test.

Should old networks get a default
carrier on load? <span class="hl">[D1]</span>

One sentence: the model failed because
one bus had no carrier label.

1. Merge the fix.
2. Decide <span class="hl">(D1)</span>.

Ledger: +D1 Default carrier on load</code></pre>

</div>
</div>

<!--
The output style changes how the agent talks, not what it does. Answer first, short sentences, every term explained.
The codes in brackets are the trick: "do D1" an hour later is unambiguous for both sides.
-->

---

<!-- header: 'Tracking: the ledger' -->

## Recommendation: a ledger that survives rewinds

<div class="cols w">
<div>

- `hooks/ledger.py` tracks **G P D B I U** items
- Rebuilt from the active transcript chain, so rewinds and compactions do not lose items
- Re-injects the open items on every prompt
- Blocks the reply if a code has no ledger entry
- Status line links the file; `/ledger` opens it in Zed

</div>
<div>

<pre><code>Ledger: <span class="hl">+D3</span> Pick store format
      | <span class="hl">-U1</span>
      | <span class="hl">xI2</span> not reproducible
      | <span class="hl">~B1</span> new text
      | <span class="hl">&gt;U2</span> owner/repo#123</code></pre>

<div class="ops">
<code>+</code><span>open, needs text</span>
<code>-</code><span>resolve</span>
<code>x</code><span>drop, with a reason</span>
<code>~</code><span>replace the text</span>
<code>&gt;</code><span>hand off to a GitHub issue, closes it here</span>
</div>

</div>
</div>

<!--
The ledger is a hook. Each reply ends with one delta line, and the hook folds those lines into a list of open items.
It walks the live transcript chain, so a rewind removes exactly the items from the rewound turns. The arrow operator hands an item off to a GitHub issue and closes it here.
-->

---

<!-- header: 'Tracking: habits' -->

## Recommendation: make every outcome traceable

- `plan-open-items`: wrap-up of open PRs, issues, decisions and cleanup
- Agent reports end with **DECISIONS** and **DEFERRED** fields
- Review issues carry `[task-related]` or `[drive-by]` tags
- Work in the current worktree, so changes appear live in Zed
- `plan-voice-handoff`: talk the session through in Claude Desktop

> Lesson: nothing important should exist only in scrollback.

<!--
A few smaller habits. Every sub-agent report has a DECISIONS and a DEFERRED field, so nothing is silently skipped.
Review findings are tagged, so drive-by issues do not creep into the change. For thinking time, the session can move to Claude Desktop and be talked through by voice.
-->

---

<!-- class: p5 -->
<!-- header: 'Quality' -->

## Recommendation: counter the habits, split the roles

<div class="cols">
<div>

### Rules in `CLAUDE.md`
- Fail fast, no gentle error handling
- No comments in code
- Typing annotations, no `hasattr`
- Parametrized pytest, reuse fixtures
- Mocks only at external boundaries

</div>
<div>

### Process
- Writer and reviewer are different agents
- The lead re-runs the tests itself
- Review rubric: *signal over noise*, with explicit do-NOT-flag lists and evidence for every issue
- `code-fix-bug`: failing test first
- `issue-raise`: minimal reproducible example

</div>
</div>

> Lesson: rules shape the writer; a separate reviewer catches what rules miss.

<!--
Each bad habit from the motivation has a rule against it in CLAUDE.md. Rules alone are not enough, so the process separates writer and reviewer.
The review rubric is as much about what not to flag as what to flag, and every issue needs evidence or it is dropped.
-->

---

<!-- class: p6 -->
<!-- header: 'Adopt' -->

## Where to start

1. Copy the output style: answer first, reference codes
2. Add `context-warn.sh` and the context meter
3. Pick one orchestration skill: `sub-run` or `sub-implement`

<p class="close">An orchestrating main agent, written-down decisions, a second pair of eyes.</p>

<p class="muted small">Every recommendation is a plain file in <code>~/.claude</code>. Copy any part into yours.</p>

<!--
You do not need all of it. Start with the output style and the context warning; they cost nothing and help on day one.
Then add one orchestration skill and watch the sessions get smaller.
-->
