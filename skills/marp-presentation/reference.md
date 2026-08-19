# Marp reference

## CLI

```bash
CHROME_PATH=/usr/bin/chromium-browser \
  npx --yes @marp-team/marp-cli@latest slides.md \
    --theme-set theme.css --allow-local-files --pdf -o slides.pdf
```

| Flag | Why |
|---|---|
| `--theme-set theme.css` | Registers the custom theme (matched by `theme:` in front-matter). |
| `--allow-local-files` | Required so local images (logos, SVGs) embed in the PDF — without it they render blank. |
| `--pdf` / `--html` / `--pptx` | Output format. `--preview` = live watch, `--watch` = rebuild on save. |
| `CHROME_PATH` | Path to a local Chromium/Chrome so Marp skips downloading its own. |
| `-o` | Output file. |

First `npx` run downloads `marp-cli` (needs network); later runs are cached.

## Front-matter

```markdown
---
marp: true
theme: <name>          # must match /* @theme <name> */ in the CSS
paginate: true
size: 16:9
header: 'Eyebrow text'
footer: 'Footer text'
---
```

## Per-slide (spot) directives

Placed at the top of a slide (after the `---` separator), underscore = this slide only:

```markdown
<!-- _class: lead -->      # apply a class to this section
<!-- _paginate: false -->  # hide page number on this slide
<!-- _header: '' -->       # clear the global header/footer for this slide
<!-- _footer: '' -->
```

Slides are separated by `---`. HTML is allowed inline (`<div>`, `<img>`, `<p class>`)
for custom layouts — style the classes in the theme.

## Theme CSS essentials

- First line must be the marker comment: `/* @theme <name> */`
- Import the base: `@import 'default';` (and `@import url(fonts)` before other rules).
- Every slide is a `section`. Set base type/color/layout there.
- `em`-based type scale off `section { font-size }` — bumping one value rescales all.
- **Pagination** needs the Marpit attribute or Marp strips the rule:
  ```css
  section::after {
    content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
  }
  ```
- `header` / `footer` are positioned boxes — restyle them (mono eyebrow, etc.).
- Fonts: `@import url('https://fonts.googleapis.com/css2?family=...')` embeds at
  render time (Chromium fetches them). Provide web-safe fallbacks in the stack.

## Gotchas

- **Blank logos in PDF** → missing `--allow-local-files`.
- **Header height drifts between slides** → the default theme vertically centers
  content; add `display:flex; flex-flow:column; justify-content:flex-start` to
  `section` so headings top-align.
- **Split/grid layout swallows the heading** → in a `display:grid` section, span
  full width explicitly: `section.split h2 { grid-column: 1 / -1; }`.
- **Screenshots can't write to some temp dirs** → render to the deck's `assets/`
  or the scratchpad, then Read it.
- **Clickable tag link** → wrap the URL in a code span inside a link:
  `[`\``github.com/...`\``](https://github.com/...)` and style `a code`.

## Verify

```bash
pdftoppm -png -r 90 slides.pdf /tmp/slide   # one PNG per page
```
Read each PNG and check alignment, color, overflow. Do this every build.
