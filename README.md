# hackingbiology.com

Website and blog of the **HackingBiology** organization — a static site built with
[Hugo](https://gohugo.io) and published by GitHub Pages from `/docs`.

Related: **biohack.it** is the software/initiative (repo `hackingbiology/biohackit`).

## Editing the site

Everything you would want to change is Markdown or TOML, editable from the GitHub web
UI, from any Markdown editor that commits, or by asking Claude.

| To change… | Edit |
|---|---|
| A post | `content/posts/<slug>.md` |
| The homepage text | `content/_index.md` |
| The About page | `content/about.md` |
| The navigation menu | `config/_default/menus.en.toml` |
| Site title, author, description | `config/_default/languages.en.toml` |
| Layout, colours, what each page shows | `config/_default/params.toml` |
| Core settings (URLs, permalinks) | `config/_default/hugo.toml` |

Commit to `main` and the **Build site** workflow rebuilds `/docs` within a minute.
Nothing else is required — no local tools, no Hugo install.

### Adding a post

Create `content/posts/my-new-post.md`:

```markdown
---
title: "My new post"
date: 2026-08-20T10:00:00+02:00
slug: my-new-post
summary: "One line that shows up in the archive and the feed."
---

Body in Markdown. Images go in `static/` and are referenced as `/path/inside/static`.
```

The URL follows the date and slug: `/2026/08/20/my-new-post/`.

## Working locally (optional)

```bash
./tools/serve.sh          # preview on http://localhost:1313
./tools/build.sh          # build into docs/ exactly as CI does
```

Never run `hugo server` directly against `docs/`: a development build writes
`Disallow: /` into `robots.txt`. `tools/serve.sh` renders elsewhere for that reason.

## Migrated from WordPress.com

The site ran on WordPress.com until August 2026. The migration preserved every
public address — see [notes/migration.md](notes/migration.md) for exactly what was
kept, what changed, and how it is verified:

```bash
python tools/verify_migration.py     # 10/10 URLs, all images, all internal links
```

## Going live on the custom domain

While the domain still points at WordPress.com, the site is previewed at
`https://hackingbiology.github.io/hackingbiology.com/`. To switch:

1. Put `hackingbiology.com` in **`static/CNAME`** (not `docs/CNAME` — Hugo rewrites `docs/`).
2. Point the DNS at GitHub Pages and set the custom domain in the repo settings.

The build reads `static/CNAME` and rebuilds every URL against the real domain
automatically.
