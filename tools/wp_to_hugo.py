# -*- coding: utf-8 -*-
"""Convert the WordPress.com backup into Hugo content, preserving URLs, images and links.

Usage:  python tools/wp_to_hugo.py [backup_dir]

Guarantees:
  * every published post keeps its exact WordPress URL  (/YYYY/MM/DD/slug/)
  * every image keeps its exact WordPress path          (/wp-content/uploads/YYYY/MM/file)
  * internal links are rewritten to site-relative form, external links untouched
  * unpublished drafts are written OUTSIDE the repo (this repo is public)
"""
import io, json, os, re, shutil, sys, html
from urllib.parse import urlsplit, unquote
from markdownify import markdownify

BACKUP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.expanduser("~"), "hackingbiology-refs", "site-backup-2026-08-18", "backup", "2026-08-18")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(REPO, "content", "posts")
STATIC = os.path.join(REPO, "static")
DRAFTS_OUT = os.path.join(os.path.expanduser("~"), "hackingbiology-refs", "drafts-markdown")

# every host WordPress ever served this site's assets from
HOSTS = ("hackingbiology.com", "www.hackingbiology.com", "hackingbiologycom.wordpress.com",
         "hackingbiologycom.files.wordpress.com")
CDN = re.compile(r"https?://i[0-9]\.wp\.com/(?:" + "|".join(h.replace(".", r"\.") for h in HOSTS) + r")")
INTERNAL = re.compile(r"https?://(?:" + "|".join(h.replace(".", r"\.") for h in HOSTS) + r")")

report = {"posts": [], "drafts": [], "media_copied": [], "media_missing": [], "links_rewritten": 0}


def load(name):
    return json.load(io.open(os.path.join(BACKUP, name), encoding="utf-8"))


def clean_text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).replace("\xa0", " ").strip()


def rewrite_urls(text):
    """Absolute self-referencing URLs -> site-relative. Strips WP resize queries."""
    global report
    n = [0]

    def strip_query(m):
        u = m.group(0)
        # /wp-content/uploads/2024/07/image.png?w=986  ->  same path, no query
        return re.sub(r"\?(w|h|ssl|resize|fit|quality)=[^\"'\s)]*", "", u)

    text = CDN.sub("", text)          # i0.wp.com proxy prefix
    text = INTERNAL.sub("", text)     # own hosts -> root-relative
    before = text
    text = re.sub(r"/wp-content/uploads/[^\"'\s)<>]+", strip_query, text)
    text = re.sub(r"(?<=[\"'(])//+", "/", text)
    n[0] = sum(1 for _ in re.finditer(r"(?:\"|\()/(?:wp-content|\d{4}/)", text))
    report["links_rewritten"] += n[0]
    return text


def to_markdown(content_html):
    h = content_html or ""
    h = re.sub(r"<!--\s*/?wp:[^>]*?-->", "", h)                       # Gutenberg block comments
    h = re.sub(r'<figure class="wp-block-embed[^>]*>.*?<div class="wp-block-embed__wrapper">\s*',
               "", h, flags=re.S)                                      # embed chrome -> bare URL
    h = re.sub(r"</div>\s*(<figcaption.*?</figcaption>)?\s*</figure>", "", h, flags=re.S)
    h = rewrite_urls(h)
    md = markdownify(h, heading_style="ATX", bullets="-", strip=["script", "style"])
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    md = re.sub(r"^\s*(https?://\S+)\s*$", r"<\1>", md, flags=re.M)    # bare URLs stay clickable
    return md + "\n"


def front_matter(p, is_draft):
    title = clean_text(p.get("title")) or "Untitled"
    cats = [c for c in (p.get("categories") or {}) if c.lower() not in ("senza categoria", "uncategorized")]
    tags = list(p.get("tags") or {})
    summary = clean_text(p.get("excerpt"))[:300]
    fm = ["---", 'title: "%s"' % title.replace('"', '\\"'), "date: %s" % p.get("date")]
    if p.get("modified") and p["modified"][:10] != (p.get("date") or "")[:10]:
        fm.append("lastmod: %s" % p["modified"])
    fm.append("slug: %s" % (p.get("slug") or ""))
    if summary:
        fm.append('summary: "%s"' % summary.replace('"', '\\"'))
    if cats:
        fm.append("categories: [%s]" % ", ".join('"%s"' % c for c in cats))
    if tags:
        fm.append("tags: [%s]" % ", ".join('"%s"' % t for t in tags))
    if is_draft:
        fm.append("draft: true")
    fm += ["wordpress_id: %s" % p["ID"], "---", ""]
    return "\n".join(fm)


# ---------------------------------------------------------------- media
def copy_media():
    media = load("media.json")
    src_dir = os.path.join(BACKUP, "media")
    for m in media:
        url = m.get("URL") or ""
        path = unquote(urlsplit(url).path).lstrip("/")          # wp-content/uploads/YYYY/MM/file
        if not path:
            continue
        src = os.path.join(src_dir, "%s-%s" % (m["ID"], os.path.basename(path)))
        dst = os.path.join(STATIC, *path.split("/"))
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            report["media_copied"].append("/" + path)
        else:
            report["media_missing"].append("/" + path)


# ---------------------------------------------------------------- posts
def write_posts():
    os.makedirs(CONTENT, exist_ok=True)
    os.makedirs(DRAFTS_OUT, exist_ok=True)
    for p in load("posts.json"):
        is_draft = p["status"] != "publish"
        slug = p.get("slug") or re.sub(r"[^a-z0-9]+", "-", clean_text(p.get("title")).lower()).strip("-")
        body = front_matter(p, is_draft) + to_markdown(p.get("content"))
        if is_draft:
            # public repo: unpublished drafts stay outside it until Fabio decides
            fn = os.path.join(DRAFTS_OUT, "%s-%s.md" % (p["ID"], slug or "untitled"))
            report["drafts"].append(os.path.basename(fn))
        else:
            fn = os.path.join(CONTENT, "%s.md" % slug)
            d = p["date"][:10].split("-")
            report["posts"].append({"slug": slug, "wp_url": "/%s/%s/%s/%s/" % (d[0], d[1], d[2], slug),
                                    "id": p["ID"], "title": clean_text(p.get("title"))})
        io.open(fn, "w", encoding="utf-8", newline="\n").write(body)


if __name__ == "__main__":
    copy_media()
    write_posts()
    io.open(os.path.join(REPO, "notes", "migration-report.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps(report, ensure_ascii=False, indent=2))
    print("posts:      %d" % len(report["posts"]))
    print("drafts:     %d  -> %s (fuori dal repo)" % (len(report["drafts"]), DRAFTS_OUT))
    print("media:      %d copiati, %d mancanti" % (len(report["media_copied"]), len(report["media_missing"])))
    for m in report["media_missing"]:
        print("  ! manca:", m)
