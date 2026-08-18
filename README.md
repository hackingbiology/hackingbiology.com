# hackingbiology.com

Website and blog of the **HackingBiology** organization.

Related: **biohack.it** is the software/initiative (repo `hackingbiology/biohackit`).
This repo covers the organization's public site only.

## Where the site runs today

| | |
|---|---|
| Platform | WordPress.com "simple" site |
| Site | `hackingbiologycom.wordpress.com`, ID **221097453** |
| Domain | hackingbiology.com (mapped) |
| Plan | Personal — no plugins, no custom CSS, free themes only |
| Theme | Twenty Twenty-Three (block theme, Site Editor) |

See [docs/site-inventory-2026-08-18.md](docs/site-inventory-2026-08-18.md) for the full
content inventory taken before any change.

## How the site is managed

Changes are made through the **WordPress.com REST API v1.1** with an OAuth token
(scope `global`). Credentials are stored **outside this repo**, in
`%USERPROFILE%\.hackingbiology\` — never committed.

```bash
tools/wp.sh "sites/221097453/posts/?number=5"     # any REST v1.1 path
python tools/wp_backup.py                          # full read-only backup
```

Getting a token (one-off, done 2026-08-18): OAuth authorization-code flow against the
app registered at developer.wordpress.com/apps. The account owner performs the login and
the authorization in their own browser; only the resulting `code` is exchanged for a token.

## Backups

Full backups (posts incl. drafts, pages, media, settings) are written **outside this
repo** — they contain unpublished drafts and the admin email address, and this repo is
public. Current backup: `C:\Users\admin\hackingbiology-refs\site-backup-2026-08-18\`.
