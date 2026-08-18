# WordPress.com → Hugo migration

Done 2026-08-18. Source of truth for the migration decisions.

## What the site was

A WordPress.com "simple" site (ID 221097453) on the Personal plan, theme Twenty
Twenty-Three, running since July 2023: 10 published posts, 20 unpublished drafts,
1 page, 28 media files, no menu, no tags, one catch-all category.
Full pre-migration inventory: [site-inventory-2026-08-18.md](site-inventory-2026-08-18.md).

## What was preserved, and how

**Post URLs — identical.** WordPress used dated permalinks. `config/_default/hugo.toml`
sets `posts = "/:year/:month/:day/:slug/"`, and each post carries its original `slug`,
so `/2024/07/20/hbot-protocol-protoco/` is the same address it always was.
Do not change that permalink pattern.

**Image and file URLs — identical.** Media was placed under
`static/wp-content/uploads/YYYY/MM/`, mirroring the WordPress upload paths, so every
old image and PDF link still resolves — including links from outside the site.
WordPress resize queries (`?w=986`) were dropped; the full-size file is served instead.

**Internal links — rewritten, same destination.** Links that pointed at
`hackingbiology.com`, `hackingbiologycom.wordpress.com` or the `i0.wp.com` CDN were
made site-relative. External links were left untouched.

**Legacy entry points**

| Old address | Now |
|---|---|
| `/home/` (the WordPress page) | redirects to `/` |
| `/category/senza-categoria/` | redirects to `/posts/` |
| `/feed/` | redirect page → `/index.xml` |

**The feed caveat.** GitHub Pages serves only `index.html` for a directory, so the RSS
XML cannot sit at `/feed/` itself. The real feed is `/index.xml` (also copied to
`/feed/index.xml`), and `/feed/` is an HTML redirect. Browsers follow it; some feed
readers will not. The site had 4 subscribers at migration time.

**`wordpress_id`** is kept in each post's front matter, so anything can be traced back
to the original.

## What deliberately did not come across

**The 20 unpublished drafts.** They were converted to Markdown but written to
`~/hackingbiology-refs/drafts-markdown/`, **outside this repo** — this repo is public
and the drafts are not. Moving them in later is a copy away, once Fabio decides which
ones to finish. Nothing was lost.

**The "Senza categoria" category** was dropped from post front matter: it carried no
information (all 10 posts had it and nothing else). The old archive URL still redirects.

## Verification

`python tools/verify_migration.py` checks the built site against the WordPress backup:

- all 10 published URLs exist
- every referenced image, PDF and internal link resolves to a real file
- every one of the 28 media files is published
- each post's rendered text is not shorter than the WordPress original
- the legacy entry points exist

It is also enforced in CI, in reduced form, on every build.

## The backup

`~/hackingbiology-refs/site-backup-2026-08-18/` — full API dump (posts incl. drafts,
pages, media binaries, settings, users) taken before anything was touched. Outside the
repo, deliberately. Regenerate with `python tools/wp_backup.py <stamp>`.

The WordPress.com site was **not modified** during the migration: everything was read
through the REST API.
