# Keeping Claude Code focused, traceable and honest

Marp deck built from `~/.claude` (README, CLAUDE.md, output style, hooks, agents, skills); 15-minute talk, 16 slides, speaker notes in HTML comments.

```
slides.md    # the deck
theme.css    # custom theme
Makefile     # build shortcuts
assets/      # logos, images, motifs
```

## Build

```bash
make preview     # live preview, reloads on save
make pdf         # → slides.pdf  (also: html, pptx)
make clean       # remove artifacts
```

`CHROME_PATH` defaults to `/usr/bin/chromium-browser`; override with e.g.
`make pdf CHROME_PATH=/snap/bin/chromium`. Web fonts load from Google Fonts at
render time, so keep network on for the build.

## Editing

- **Content** — `slides.md`; slides split by `---`, per-slide layout via spot
  directives (`<!-- _class: lead -->` title). `<!-- class: pN -->` (p1..p6) sets the talk-timeline rail at the top; `<!-- header: ... -->` names the section.
- **Look** — `theme.css` (`dispatch`): steel-grey paper, navy ink, one amber accent; Archivo + JetBrains Mono. Rail segments are proportional to the minutes per section. Build uses `--html` for the inline diagrams.

Outputs are gitignored — regenerate with `make`.
