#!/usr/bin/env python3
"""Build a dependency-light local preview of the Jekyll site into _site.

GitHub Pages renders _layouts and _includes in production. This helper mirrors
the shared shell locally so the site can be reviewed without installing Ruby
gems on a new machine.
"""

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
SITE_URL = "https://xxialab.github.io"


def read_page(path: Path) -> tuple[dict, str]:
    source = path.read_text()
    if not source.startswith("---\n"):
        raise ValueError(f"Missing front matter: {path}")
    _, raw_meta, content = source.split("---\n", 2)
    meta = {}
    for line in raw_meta.splitlines():
        key, value = line.split(":", 1)
        value = value.strip()
        if value == "null":
            meta[key] = None
        elif value.startswith('"'):
            meta[key] = json.loads(value)
        else:
            meta[key] = value
    return meta, content.lstrip()


def nav_link(label: str, href: str, key: str, active: str) -> str:
    current = key == active
    css = "nav-item active" if current else "nav-item"
    aria = ' aria-current="page"' if current else ""
    return f'<a class="{css}" href="{href}"{aria}>{label}</a>'


def render_header(meta: dict) -> str:
    zh = meta["lang"] == "zh-Hans"
    if zh:
        items = [
            ("首页", "/zh/index.html", "home"),
            ("研究方向", "/zh/research.html", "research"),
            ("成员", "/zh/people.html", "people"),
            ("发表成果", "/zh/publications.html", "publications"),
            ("教学", "/zh/teaching.html", "teaching"),
            ("职位空缺", "/zh/vacancies.html", "vacancies"),
        ]
        home, menu_label, nav_label, home_label = "/zh/index.html", "菜单", "主导航", "CSLM Lab 首页"
        lang_label = "English"
    else:
        items = [
            ("Home", "/index.html", "home"),
            ("Research", "/research.html", "research"),
            ("People", "/people.html", "people"),
            ("Publications", "/publications.html", "publications"),
            ("Teaching", "/teaching.html", "teaching"),
            ("Vacancies", "/vacancies.html", "vacancies"),
        ]
        home, menu_label, nav_label, home_label = "/index.html", "Menu", "Primary navigation", "CSLM Lab home"
        lang_label = "中文"
    links = "\n          ".join(nav_link(*item, meta["nav"]) for item in items)
    return f'''<header>
  <nav aria-label="{nav_label}">
    <div class="brand">
      <a href="{home}" aria-label="{home_label}">
        <img class="brand-wordmark" src="/images/logo/cslm-wordmark.svg" alt="" width="690" height="205">
        <span class="brand-meta"><b>LAB</b><span>SUSTech</span></span>
      </a>
    </div>
    <details class="site-menu">
      <summary>{menu_label}</summary>
      <div class="nav-panel">
          {links}
      </div>
    </details>
    <a class="lang-switch" href="{meta['alternate']}" hreflang="{meta['alt_lang']}" lang="{meta['alt_lang']}">{lang_label}</a>
  </nav>
</header>'''


def render_page(meta: dict, content: str) -> str:
    title = html.escape(meta["title"])
    description = html.escape(meta["description"], quote=True)
    canonical = SITE_URL + meta["permalink"]
    alternate = SITE_URL + meta["alternate"]
    x_default = SITE_URL + meta["x_default"]
    locale = "zh_CN" if meta["lang"] == "zh-Hans" else "en_US"
    skip = "跳到正文" if meta["lang"] == "zh-Hans" else "Skip to content"
    analytics = (ROOT / "_includes" / "analytics.html").read_text().strip()
    footer = (ROOT / "_includes" / "footer.html").read_text().strip()
    return f'''<!DOCTYPE html>
<html lang="{meta['lang']}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | CSLM Lab</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#f6f8f7">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="{meta['alt_lang']}" href="{alternate}">
  <link rel="alternate" hreflang="x-default" href="{x_default}">
  <link rel="icon" href="/images/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/style.css?v=20260828-11">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="CSLM Lab">
  <meta property="og:title" content="{title} | CSLM Lab">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE_URL}/images/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="{locale}">
</head>
<body>
  <a class="skip-link" href="#main-content">{skip}</a>
  {render_header(meta)}
  {content.strip()}
  {footer}
  <script defer src="/assets/site.js?v=20260828-1"></script>
  {analytics}
</body>
</html>
'''


def copy_assets() -> None:
    shutil.copytree(ROOT / "assets", OUT / "assets")
    excluded = {"Asset 7.pdf", "images.key", "test1.png", "profile.JPG", "profile copy.JPG", ".DS_Store"}
    shutil.copytree(
        ROOT / "images",
        OUT / "images",
        ignore=lambda _directory, names: [name for name in names if name in excluded],
    )


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    copy_assets()
    page_paths = sorted(ROOT.glob("*.html")) + sorted((ROOT / "zh").glob("*.html"))
    for source in page_paths:
        meta, content = read_page(source)
        output = OUT / source.relative_to(ROOT)
        output.parent.mkdir(parents=True, exist_ok=True)
        if meta.get("layout") is None or meta.get("layout") == "null":
            output.write_text(content)
        else:
            output.write_text(render_page(meta, content))
    print(f"Built {len(page_paths)} pages in {OUT}")


if __name__ == "__main__":
    main()
