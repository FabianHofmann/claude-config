---
name: doc-slides
description: Create presentation slides / slide decks from notes using Marp (Markdown → PDF/HTML/PPTX), styled with the frontend-design skill. Use when the user wants to make a presentation, slide deck, slides, or a talk from Markdown/notes.
---

# Marp Presentation

Build a production slide deck in Markdown with Marp, give it a distinctive custom
theme via the `frontend-design` skill, and ship it with a Makefile + README.

## Workflow

1. **Scope it.** Get the source notes and the subject. If layout/brand isn't
   pinned, propose one and proceed. Decide slide count (usually 4–6 for an intro).

2. **Scaffold** the deck directory (copy the templates in `assets/`):
   ```
   <deck>/
   ├── slides.md      # the deck            (from assets/example-deck.md)
   ├── theme.css      # custom Marp theme   (from assets/example-theme.css)
   ├── Makefile       # build shortcuts     (from assets/Makefile)
   ├── README.md      # build/edit docs     (from assets/README.md)
   └── assets/        # logos, motifs, images
   ```
   Rename `theme` consistently: the CSS first line `/* @theme <name> */`, the
   deck front-matter `theme: <name>`, and `THEME` in the Makefile must all match.

3. **Style it — invoke the `frontend-design` skill first.** Do not reuse the
   example theme's look verbatim. Run `frontend-design` to derive a palette,
   type pairing, layout, and one signature element *specific to this subject*,
   then encode those decisions in `theme.css`. The example theme shows the token
   structure to fill in (`:root` custom properties, `em`-based type scale), not a
   look to copy. Keep any explicit user constraints (e.g. header color, bullet
   style) across restyles.

4. **Write the deck** in `slides.md`: Marp front-matter, slides split by `---`,
   per-slide layout via spot directives (`<!-- _class: lead -->` etc.). Write real
   copy, not lorem. See `reference.md` for the directive set.

5. **Build and verify visually — always.**
   ```bash
   cd <deck> && make pdf
   pdftoppm -png -r 90 slides.pdf /tmp/slide   # then Read the PNGs
   ```
   Render every slide to PNG and look at it. Iterate on the CSS until it's right —
   never ship a deck you haven't seen rendered. `make preview` gives a live
   auto-reloading preview while editing.

## Key mechanics (details in `reference.md`)

- Register the theme with `--theme-set theme.css`; embed local images with
  `--allow-local-files`; point Marp at a local browser via `CHROME_PATH`. The
  Makefile wraps all three.
- Web fonts (`@import url(...)` from Google Fonts) load and embed at render time —
  keep network on for the build.
- Pagination CSS **must** use `content: attr(data-marpit-pagination) ...` or Marp
  discards the rule.
- Markdown links become clickable annotations in the PDF.

## Files

- `assets/example-deck.md` — deck skeleton (front-matter + lead/split/closing slides)
- `assets/example-theme.css` — worked theme showing the token system to adapt
- `assets/Makefile` — `make preview|pdf|html|pptx|clean`
- `assets/README.md` — README template for the deck folder
- `reference.md` — Marp directives, CLI flags, and the gotchas
