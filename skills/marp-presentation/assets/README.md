# <deck title>

Marp deck built from `<source notes>`.

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
  directives (`<!-- _class: lead -->` title, `<!-- _class: split -->` two columns).
- **Look** — `theme.css`; one accent token drives everything, the type scale is
  `em`-based off `section { font-size }`.

Outputs are gitignored — regenerate with `make`.
