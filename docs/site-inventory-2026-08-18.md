# hackingbiology.com — inventory before any change

Taken 2026-08-18 via WordPress.com REST API v1.1 (`context=edit`), read-only.
Full backup: `C:\Users\admin\hackingbiology-refs\site-backup-2026-08-18\` (23 MB, outside the repo).

## Platform

| | |
|---|---|
| Site | `hackingbiologycom.wordpress.com` — ID 221097453 |
| Admin | `eclecticismnow` |
| Plan | **Personal** — no plugins, no custom CSS, free themes only |
| Theme | **Twenty Twenty-Three** 1.6 (block theme → Site Editor available) |
| Language | en (`lang_id` 1) · public (`blog_public` 1) |

## Content

| | Count |
|---|---|
| Published posts | **10** (2023-07-09 → 2025-08-14) |
| Draft posts | **20** (real research notes, not empty autosaves) |
| Pages | **1** — `home` (ID 2) |
| Categories | 1 — "Senza categoria" (all 10 posts) |
| Tags | **0** |
| Media | 28 (25 png, 2 jpg, 1 pdf) |
| Menus | **0** — `menus: []`, `locations: []` |

### Published posts

| Date | Slug |
|---|---|
| 2025-08-14 | pills-management |
| 2025-03-16 | nutritional-epigenetic |
| 2025-01-13 | increasing-oxygen-while-sleeping |
| 2025-01-01 | many-protocols-for-many-pills |
| 2024-12-15 | measurements-of-biological-age |
| 2024-07-20 | glucose-and-rapamycin-for-anti-aging |
| 2024-07-20 | hbot-protocol-protoco |
| 2024-07-19 | project-update-july-2024 |
| 2024-01-07 | software-review |
| 2023-07-09 | a-data-driven-applied-aging-research-project |

### Draft backlog

20 drafts, ~13k characters total. Titles (newest first): Unrolling home HBOT ·
Telomere how to? · Setting up your own HBOT antiaging · Measuring cellular senescence ·
Lowering Homocysteine to safest low-level? · Vitamin E on biomarkers ·
Multiple targets for anti-aging · Vascular endothelial care · Plasmapheresis for antiaging ·
Epigenetic Drugs: We're not yet there · DNA Analytics for Longevity ·
Stem Cells Therapy: Antiaging? · On Dyslipidemia & Cardiovascular Disease ·
Metabolic manipulation via ketone · Physical Exercise & Laziness ·
Atherosclerotic cardiovascular disease (ASCVD) anti-aging · senolytics autophagy research ·
Wholesale sourcing · Blood Panel for Longevity Monitoring · Aging Biological Targets

Drafts are **not** reproduced in this repo — it is public and they are unpublished.

## Issues found

1. **No menu exists.** The About / Home / Contact items visible on the live site are the
   theme template's placeholder navigation block: all three link to `#`. There is nothing
   to edit — a menu must be created, together with the destination pages, which do not exist.
2. **Front-page setting is inconsistent**: `show_on_front = page` but `page_on_front = 0`,
   so the site falls back to the post listing. The `home` page exists but is assigned to nothing.
3. **No taxonomy**: 1 catch-all category, 0 tags, across 30 pieces of content spanning
   HBOT / epigenetics / biomarkers / senolytics.
4. **20 drafts stalled** — an editorial backlog, not junk.
