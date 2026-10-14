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

<div class="legend"><span>Why</span><span>Anatomy</span><span>Context</span><span>Attention</span><span>Trust</span><span>Team</span><span>Adopt</span></div>

# Keeping LLMs focused, traceable and efficient

<p class="sub">Lessons learned on how to setup Claude Code for day-to-day work, alone and in a team</p>

<p class="who">Fabian Hofmann, Open Energy Transition</p>

<!--
Twenty minutes of lessons learned from daily work with Claude Code, alone and in a team, and what we recommend as a result. Most recommendations map to plain files in ~/.claude that you can copy.
The bar at the top of each slide is the talk timeline: grey is ahead, amber is where we are.
-->

---

<!-- class: p1 -->
<!-- header: 'Why' -->

## The agent scales. Three things do not.

<div class="limits tall">
<div><b>Context</b>what the model can hold</div>
<div><b>Attention</b>what you can follow</div>
<div><b>Trust</b>what you can merge without reading</div>
</div>

<!--
Agents now run for an hour, read dozens of files and write hundreds of lines. The human job moves from writing code to orchestrating and checking it.
Three things did not grow with the agent: the context window, your attention and your trust in the output. The limits are on the model's memory and on the human, not on the model's speed.
The rest of the talk is about these three limits, one slide each, then what helps.
-->

---

<!-- header: 'Why: context' -->

## Limit 1: the context window

<div class="cols n">
<div>

<p class="big">~200k <small>tokens</small></p>

- decreased quality
- slower
- higher costs

</div>
<div>

<h3>Every turn sends the whole history again</h3>
<div class="grow">
<p style="--k:1">turn 1</p>
<p style="--k:2">turn 2</p>
<p style="--k:3">turn 3</p>
<p style="--k:4">turn 4</p>
<p style="--k:5">turn 5</p>
</div>

</div>
</div>

> Lesson: every file the agent reads is paid for again on every later turn.

<!--
Think of the context like the memory budget of a solve. Everything the agent read stays in the window.
Past roughly 200k tokens, answers get worse, replies get slower and bills go up.
The bars: amber is the new part of each turn, navy is the history that is sent again. A file dump early in the session costs on every turn after it.
-->

---

<!-- header: 'Why: attention' -->

## Limit 2: your attention

<div class="limits num tall">
<div><b>1 <small>hour</small></b>of agent work</div>
<div><b>10</b>open threads</div>
<div><b>3</b>half-made decisions</div>
</div>

> Lesson: the bottleneck is human attention, not model speed.

<!--
Quick show of hands: who had a session go off track after a compaction?
The agent produces a lot of text and a lot of options. After an hour you have ten open threads and three half-made decisions.
A rewind or a compaction silently drops some of them. Permission prompts break the flow, and approving by reflex is unsafe.
Two weeks later, nobody can explain why a line changed.
-->

---

<!-- header: 'Why: trust' -->

## Limit 3: plausible is not good

<div class="cols w">
<div>

<pre><code><span class="hl">try:</span>
    n.optimize()
<span class="hl">except Exception:</span>
    <span class="hl"># Optimization failed, continue</span>
    <span class="hl">pass</span>
if <span class="hl">hasattr(n, "buses")</span>:
    ...</code></pre>

</div>
<div>

- errors hidden by `try/except`
- `hasattr` probing
- comments that restate the code

</div>
</div>

> Lesson: self-review is weak. The writer rarely finds its own mistakes.

<!--
The code looks fine at first glance. But it has habits that hurt in a modelling code base: swallowed solver errors, attribute probing, comments that say nothing.
Other habits: long, repetitive tests and mocks everywhere.
And if you ask the same agent to review its own work, it mostly agrees with itself.
-->

---

<!-- header: 'Why: overview' -->

## Three limits, three answers

<div class="limits tall">
<div><b>Context</b>Visible budget, sub-agents, files<div class="chips"><code>context-warn.sh</code> <code>sub-*</code> <code>plan-*</code></div></div>
<div><b>Attention</b>Skimmable output, a ledger<div class="chips"><code>standard.md</code> <code>ledger.py</code> <code>settings.json</code></div></div>
<div><b>Trust</b>Rules, a separate reviewer<div class="chips"><code>CLAUDE.md</code> <code>review-*</code></div></div>
</div>

<!--
This is the map for the rest of the talk. Each recommendation answers one limit, and each lives in a plain file you can copy.
Context: make the budget visible, orchestrate sub-agents, write the bulk to files.
Attention: skimmable output, a ledger, traceable outcomes, fewer permission prompts.
Trust: rules for the writer, a separate reviewer, the implement-review-revise loop.
-->

---

<!-- class: p2 -->
<!-- header: 'Anatomy' -->

## Where recommendations live: `~/.claude`

<div class="anat">
<div><b><code>CLAUDE.md</code></b>House rules for every project</div>
<div><b><code>output-styles/</code></b>How the agent talks</div>
<div><b><code>settings.json</code></b><span class="n">60</span> allow rules, hooks</div>
<div class="hot"><b><code>hooks/</code></b><code>context-warn.sh</code> <code>ledger.py</code></div>
<div><b><code>agents/</code></b><code>implement-review-revise</code></div>
<div><b><code>statusline-command.sh</code></b>Context meter, ledger link</div>
<div class="wide"><b><code>skills/</code></b><span class="n">36</span> skills<div class="chips"><code>plan-</code> <code>sub-</code> <code>review-</code> <code>git-</code> <code>pr-</code> <code>issue-</code> <code>ci-</code> <code>code-</code> <code>doc-</code></div></div>
</div>

<!--
Claude Code reads seven kinds of files. CLAUDE.md holds the house rules: Python style, git, delegation. The output style standard.md sets the voice. settings.json wires everything together: default model opus, 60 allow rules for shell commands, plugins, status line and hooks.
Hooks are small scripts that run on events: context-warn.sh on Stop, ledger.py on prompt, stop and compact. The status line shows model, branch, context meter and ledger link.
Skills are the bulk: 36 packaged instructions, invoked by name like /git-commit, grouped by prefix as shown so they sort together. Skills encode team workflows; the allowlist cuts permission prompts.
-->

---

<!-- class: p3 -->
<!-- header: 'Context: see it' -->

## Recommendation: make the budget visible

<div class="meter"><span class="g"></span><span class="y"></span><span class="r"></span></div>
<div class="scale"><span>0</span><span>100k</span><span>150k warn</span><span>+25k</span></div>

- Status line: green, yellow at 2/3, red at the limit
- `hooks/context-warn.sh` warns at **150k**, then every **25k**
- It suggests `/compact`, `/clear` or a sub-agent

<!--
First recommendation: make the budget visible. The status line shows a context meter that turns yellow at two thirds of the threshold and red at 150k.
The Stop hook context-warn.sh then posts a warning and repeats it every 25k tokens.
-->

---

<!-- header: 'Context: route' -->

## Recommendation: pick the model per task

<div class="limits tall">
<div class="hot"><b>Opus</b>default, day-to-day work</div>
<div><b>Sonnet</b>simple, well-scoped sub-tasks</div>
<div><b>Fable</b>hard problems and planning</div>
</div>

<!--
The model choice is the second lever on the budget. Opus by default, Sonnet for cheap sub-tasks, Fable for hard ones.
Reviews prefer Opus to save tokens.
-->

---

<!-- header: 'Context: orchestrate' -->

## Recommendation: the main agent orchestrates

<div class="flow">
<div class="st hot"><b>main agent</b>plans, decides</div>
<div class="ar">→</div>
<div class="grp">
<p>sub-agents read and edit the files</p>
<div class="row">
<div class="st"><b>implementer</b>edits, adds tests</div>
<div class="st"><b>reviewer</b>evidence</div>
<div class="st"><b>reviser</b>fixes</div>
</div>
</div>
<div class="ar">→</div>
<div class="st"><b>report</b>back to the main agent</div>
</div>

<div class="limits num two" style="margin-top:var(--gap)">
<div><b>X</b>rounds at most</div>
<div><b>300</b>words at most in the report</div>
</div>

<!--
Second recommendation: the main agent is an orchestrator. It plans, hands tasks to sub-agents and makes decisions with you. Sub-agents read the files and burn their own context; the main agent only gets the conclusion.
CLAUDE.md says: for work that you can delegate to sub-agents, do so. sub-run and sub-this hand a task to a sub-agent.
sub-implement runs the implement-review-revise lead. The lead coordinates only. The reviewer marks issues as must-fix or nice-to-have, with evidence. The reviser fixes task-related issues. At most two rounds, and the report has at most 300 words.
-->

---

<!-- header: 'Context: write it down' -->

## Recommendation: put the bulk in files

<div class="flow">
<div class="st"><b>long session</b>heavy context</div>
<div class="ar">→</div>
<div class="st hot"><b>handoff</b>≤ 40 lines, <code>plan-handoff</code></div>
<div class="ar">→</div>
<div class="st"><b>fresh session</b>clean context</div>
</div>

<p class="close">A fresh session with a good handoff beats a compacted old one.</p>

<!--
Plans live in files: plan-prepare writes the plan to dev/<topic>/plan.md, not into the chat.
When a session gets heavy, plan-handoff writes a prompt of at most 40 lines, and a fresh session starts clean.
graft is a code index: one query replaces many file reads.
-->

---

<!-- class: p4 -->
<!-- header: 'Attention: the voice' -->

## Recommendation: an output style for skimming

<div class="cols w">
<div>

<pre><code>Yes. The solve fails because bus "DE0 H2"
has no carrier <span class="hl">[F1]</span>. The fix sets it in
add_electrolysers() and adds a test.

Should old networks get a default
carrier on load? <span class="hl">[D1]</span>

One sentence: one bus had no carrier label.

1. Merge the fix.
2. Decide <span class="hl">(D1)</span>.

Ledger: <span class="hl">+D1</span> Default carrier on load</code></pre>

</div>
<div>

- Answer first, then reasons
- Short, plain sentences
- Codes to cite later: <code>F</code> <code>D</code> <code>P</code> …

</div>
</div>

<!--
The output style changes how the agent talks, not what it does. Answer first, ASD-STE100 Simplified Technical English, at most 20 words per sentence, every term glossed. One sentence to repeat to a colleague, and numbered next steps as options.
The codes in brackets are the trick: "do D1" an hour later is unambiguous for both sides.
Codes: F finding, C correction, I related issue, U unrelated issue, B breaking change, D decision, P PR or issue, G goal.
-->

---

<!-- header: 'Attention: the ledger' -->

## Recommendation: a ledger that survives rewinds

<div class="cols">
<div>

<pre><code>Ledger: <span class="hl">+D3</span> Pick store format
      | <span class="hl">-U1</span>
      | <span class="hl">xI2</span> not reproducible
      | <span class="hl">~B1</span> new text
      | <span class="hl">&gt;U2</span> owner/repo#123</code></pre>

</div>
<div class="ops">
<code>+</code><span>open, needs text</span>
<code>-</code><span>resolve</span>
<code>x</code><span>drop, with a reason</span>
<code>~</code><span>replace the text</span>
<code>&gt;</code><span>hand off to a GitHub issue</span>
</div>
</div>

<div class="limits" style="margin-top:var(--gap)">
<div><b>G P D B I U</b>items tracked</div>
<div><b>Every prompt</b>open items re-injected</div>
<div class="hot"><b>Blocks</b>a code with no entry</div>
</div>

<!--
The ledger is a hook, hooks/ledger.py. Each reply ends with one delta line, and the hook folds those lines into a list of open items.
It is rebuilt from the active transcript chain, so a rewind removes exactly the items from the rewound turns, and compactions lose nothing.
It re-injects the open items on every prompt, and blocks the reply if a code has no ledger entry. The arrow operator hands an item off to a GitHub issue and closes it here.
The status line links the file; /ledger opens it in Zed.
-->

---

<!-- header: 'Attention: habits' -->

## Recommendation: make every outcome traceable

<div class="limits tall">
<div><b>Wrap-up</b>open PRs, issues, decisions, cleanup<div class="chips"><code>plan-open-items</code></div></div>
<div><b>Agent reports</b>end with two fields<div class="chips"><code>DECISIONS</code> <code>DEFERRED</code></div></div>
<div><b>Review tags</b>keep drive-bys out<div class="chips"><code>[task-related]</code> <code>[drive-by]</code></div></div>
</div>

<!--
A few smaller habits. plan-open-items gives a wrap-up of open PRs, issues, decisions and cleanup.
Every sub-agent report has a DECISIONS and a DEFERRED field, so nothing is silently skipped.
Review findings are tagged, so drive-by issues do not creep into the change.
Work in the current worktree, so changes appear live in Zed. For thinking time, plan-voice-handoff moves the session to Claude Desktop to talk it through by voice.
Nothing important should exist only in scrollback.
-->

---

<!-- class: p5 -->
<!-- header: 'Trust' -->

## Recommendation: counter the habits, split the roles

<div class="cols eq">
<div>

<h3>Without rules</h3>

<pre><code>try:
    n.optimize()
except Exception:
    pass</code></pre>

</div>
<div>

<h3>With <code>CLAUDE.md</code>: fail fast</h3>

<pre><code>n.optimize()</code></pre>

</div>
</div>

<h3 style="margin-top:1.2em">Separate reviewers, scaled by change size</h3>

<div class="limits num">
<div><b>1</b>reviewer, ≤ 10 lines</div>
<div><b>2</b>reviewers, ≤ 100 lines</div>
<div class="hot"><b>4</b>reviewers and a coordinator, more</div>
</div>

<!--
Each bad habit from the motivation has a rule against it in CLAUDE.md: fail fast, no gentle error handling, no comments in code, typing annotations, no hasattr, parametrized pytest, reuse fixtures, mocks only at external boundaries.
Rules alone are not enough, so writer and reviewer are different agents, and the lead re-runs the tests itself. review-* runs parallel reviewers and scales the fleet with the size of the change.
The review rubric is signal over noise: explicit do-NOT-flag lists, and evidence for every issue.
code-fix-bug starts with a failing test; issue-raise needs a minimal reproducible example.
Rules shape the writer; a separate reviewer catches what rules miss.
-->

---

<!-- class: p6 -->
<!-- header: 'Team' -->

## Cheap to write, expensive to read

<div class="cols eq">
<div>

<h3>One diff, many readers</h3>
<div class="grow cost">
<p style="--k:.5">generate</p>
<p style="--k:3.6">reviewer</p>
<p style="--k:4.3">maintainer</p>
<p style="--k:5">future you</p>
</div>

</div>
<div>

<h3>The three limits, now shared</h3>
<div class="map">
<span>your attention</span><i>→</i><b>their attention</b>
<span>plausible ≠ good</span><i>→</i><b>what you share must be good</b>
<span>you decide</span><i>→</i><b>the team designs together</b>
</div>

</div>
</div>

> Lesson: your context budget becomes everyone's budget.

<!--
So far, one person and one agent. In a team, the same three limits come back, but now they are shared.
The agent writes in seconds. Every reader pays again: the reviewer, the maintainer, and you in six months.
Your attention becomes their attention. Plausible is not good becomes: what you share must be good. And the decisions move from you alone to the team.
-->

---

<!-- header: 'Team: shared spaces' -->

## Recommendation: do not bloat shared spaces

<div class="cols eq">
<div>

<h3>Generated PR body</h3>

<pre><code><span class="hl">## Summary</span>
This PR introduces a <span class="hl">comprehensive,</span>
<span class="hl">robust</span> overhaul of carrier handling.
<span class="hl">## Changes</span>
- Added <span class="hl">robust</span> error handling
- <span class="hl">Enhanced</span> maintainability …</code></pre>

</div>
<div>

<h3>Curated PR body</h3>

<pre><code>Set carrier on electrolyser buses.
Fixes #412: solve failed on "DE0 H2".
Adds test_electrolyser_carrier.
No breaking change.</code></pre>

</div>
</div>

<div class="limits" style="margin-top:var(--gap)">
<div><b>PRs</b>short, squashed<div class="chips"><code>pr-raise</code> <code>git-commit</code></div></div>
<div><b>Issues</b>one per problem, an MRE<div class="chips"><code>issue-raise</code></div></div>
<div class="hot"><b>Reviews</b>filtered, no transcripts</div>
</div>

<!--
GitHub is a shared space, and generated text bloats it fast. Left: a typical generated PR body. Right: the same change in four lines.
pr-raise keeps the body short. git-commit writes at most five lines. issue-raise files one issue per problem, always with a minimal reproducible example.
Never paste an agent transcript into a PR or issue. Filter AI review comments before you post them, and squash noisy commits.
-->

---

<!-- header: 'Team: documents' -->

## Recommendation: share less, share better

<div class="cols">
<div>

<h3>What reaches the team</h3>
<div class="limits stack">
<div class="hot"><b>Hand-written</b>best, rarest</div>
<div><b>Curated &amp; minimal</b>agent draft <div class="chips"><code>plan-prepare</code></div></div>
<div class="off"><b>Raw generated</b>never shared</div>
</div>

</div>
<div>

<h3>A design doc, four parts</h3>

<pre><code><span class="hl">## Problem</span>
   one paragraph
<span class="hl">## Decision</span>
   one file per run, netCDF
<span class="hl">## Worked example</span>
   a 3-bus network, end to end
<span class="hl">## Rejected alternatives</span>
   Parquet: no nested data</code></pre>

</div>
</div>

<p class="close">The agent drafts, a human cuts and owns it.</p>

<!--
Not everything the agent writes should reach the team. Hand-written is best. Curated and minimal is fine. Raw generated text is never shared.
A design doc has four parts: the problem, the decision, one worked example, and the alternatives we rejected and why.
plan-prepare writes the first draft. A human cuts it to the essentials and puts their name on it.
-->

---

<!-- header: 'Team: decisions' -->

<span class="tag">practice, not config</span>

## Recommendation: we are designers now, meet on decisions

<h3>Implementation is cheap. The risk moves from bad code to design drift.</h3>

<div class="flow">
<pre><code>Ledger: <span class="hl">+D4</span> Store format
      | <span class="hl">+D5</span> Carrier naming
      | <span class="hl">+D6</span> Drop the v1 API</code></pre>
<div class="ar">→</div>
<div class="st hot"><b>Design meeting, 30 min</b>1. <code>D4</code> Store format<br>2. <code>D5</code> Carrier naming<br>3. <code>D6</code> Drop the v1 API</div>
</div>

<p class="close">Design in a meeting, code review in writing.</p>

<!--
This one is a practice, not a file. The agent makes implementation cheap, so the risk moves: less bad code, more design drift. Five people, five agents, five slightly different designs.
The ledger already collects the open decisions as D items. Bring them to a short meeting and decide them together.
Then design is settled in the meeting, and code review stays in writing, on GitHub.
-->

---

<!-- class: p7 -->
<!-- header: 'Adopt' -->

## Where to start

<div class="limits num">
<div><b>1</b>Copy the output style</div>
<div><b>2</b>Add <code>context-warn.sh</code> and the meter</div>
<div><b>3</b>Pick one: <code>sub-run</code> or <code>sub-implement</code></div>
<div class="wide">In a team: one design doc, one short meeting, short PRs.</div>
</div>

<p class="close">An orchestrating main agent, written-down decisions, a second pair of eyes.</p>

<!--
You do not need all of it. Start with the output style and the context warning; they cost nothing and help on day one.
Then add one orchestration skill and watch the sessions get smaller.
Most recommendations are plain files in ~/.claude. Copy any part into yours.
In a team, start with one design doc, one short meeting and short PRs.
-->
