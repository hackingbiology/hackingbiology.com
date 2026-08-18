# -*- coding: utf-8 -*-
"""Verify the migrated site against the WordPress backup.

Checks, for the built output in docs/:
  1. every published WordPress URL exists
  2. every image/file referenced by a page resolves to a real file
  3. every internal link resolves to a real page
  4. the legacy entry points still work (/home/, /feed/, category archive)
  5. no post content was lost (text length vs the WordPress original)
"""
import io, json, os, re, sys, html
from urllib.parse import urlsplit, unquote

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")
BACKUP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.expanduser("~"), "hackingbiology-refs", "site-backup-2026-08-18", "backup", "2026-08-18")

fail, warn = [], []


def built_path(url_path):
    p = unquote(url_path).split("#")[0].split("?")[0].lstrip("/")
    # strip the project-pages prefix if the build used one
    if p.startswith("hackingbiology.com/"):
        p = p[len("hackingbiology.com/"):]
    cand = os.path.join(DOCS, *p.split("/")) if p else DOCS
    if os.path.isdir(cand):
        return os.path.join(cand, "index.html")
    return cand


def text_of(h):
    h = re.sub(r"(?s)<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


# 1 -- every published WordPress URL still exists ---------------------------
posts = json.load(io.open(os.path.join(BACKUP, "posts.json"), encoding="utf-8"))
published = [p for p in posts if p["status"] == "publish"]
for p in published:
    d = p["date"][:10].split("-")
    url = "/%s/%s/%s/%s/" % (d[0], d[1], d[2], p["slug"])
    if not os.path.exists(built_path(url)):
        fail.append("URL mancante: %s (post %s)" % (url, p["ID"]))

# 5 -- content preserved ----------------------------------------------------
for p in published:
    d = p["date"][:10].split("-")
    f = built_path("/%s/%s/%s/%s/" % (d[0], d[1], d[2], p["slug"]))
    if not os.path.exists(f):
        continue
    src_len = len(text_of(p.get("content") or ""))
    out_len = len(text_of(io.open(f, encoding="utf-8").read()))
    if src_len and out_len < src_len * 0.85:
        fail.append("contenuto accorciato: %s  (WordPress %d char -> sito %d)" % (p["slug"], src_len, out_len))
    elif src_len and out_len < src_len * 0.95:
        warn.append("contenuto piu' corto del 5%%: %s (%d -> %d)" % (p["slug"], src_len, out_len))

# 2 + 3 -- references resolve ----------------------------------------------
pages = [os.path.join(r, f) for r, _, fs in os.walk(DOCS) for f in fs if f.endswith(".html")]
refs, checked = {}, 0
for f in pages:
    h = io.open(f, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r'(?:src|href)=(?:"([^"]+)"|\'([^\']+)\'|([^\s>]+))', h):
        u = m.group(1) or m.group(2) or m.group(3)
        if not u or u.startswith(("#", "mailto:", "data:", "javascript:")):
            continue
        sp = urlsplit(u)
        if sp.netloc and sp.netloc not in ("hackingbiology.com", "hackingbiology.github.io"):
            continue                                   # external link, left untouched by design
        if not sp.path or sp.path.startswith("//"):
            continue
        refs.setdefault(sp.path, set()).add(os.path.relpath(f, DOCS))

for path, sources in sorted(refs.items()):
    checked += 1
    if not os.path.exists(built_path(path)):
        kind = "immagine/file" if re.search(r"\.(png|jpe?g|gif|pdf|svg|webp)$", path, re.I) else "link"
        fail.append("%s rotto: %s  (in %s)" % (kind, path, ", ".join(sorted(sources)[:2])))

# 4 -- legacy entry points --------------------------------------------------
for legacy, what in [("/home/", "vecchia pagina Home"), ("/feed/", "feed RSS"),
                     ("/category/senza-categoria/", "archivio categoria"), ("/", "homepage")]:
    p = built_path(legacy)
    if legacy == "/feed/":
        p = os.path.join(DOCS, "feed", "index.xml")
    if not os.path.exists(p):
        fail.append("%s mancante: %s" % (what, legacy))

# media parity
media = json.load(io.open(os.path.join(BACKUP, "media.json"), encoding="utf-8"))
missing_media = [m["URL"] for m in media
                 if not os.path.exists(os.path.join(DOCS, *unquote(urlsplit(m["URL"]).path).lstrip("/").split("/")))]
for u in missing_media:
    fail.append("media non pubblicato: %s" % urlsplit(u).path)

print("post pubblicati verificati : %d" % len(published))
print("riferimenti interni testati: %d" % checked)
print("media nel sito             : %d/%d" % (len(media) - len(missing_media), len(media)))
print("")
if warn:
    print("AVVISI (%d):" % len(warn))
    for w in warn:
        print("  ~", w)
if fail:
    print("ERRORI (%d):" % len(fail))
    for f_ in fail:
        print("  !", f_)
    sys.exit(1)
print("OK - nessun URL, immagine o link interno perso.")
