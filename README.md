# CSLM Lab website

The site is a bilingual Jekyll site for GitHub Pages. Shared document structure lives in `_layouts/default.html`; navigation, footer, and analytics live in `_includes/`. Page files contain front matter plus their page-specific `<main>` content.

## Local preview

Build a dependency-light preview and serve the generated directory:

```bash
python3 scripts/build_preview.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory _site
```

GitHub Pages uses Jekyll directly in production. The local helper exists so contributors do not need a Ruby toolchain just to review HTML and CSS changes.

Use `vacancies.html` for all new links. The misspelled legacy `valencies.html` addresses are retained only as redirects so existing bookmarks continue to work.
