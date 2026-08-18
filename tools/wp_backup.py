# -*- coding: utf-8 -*-
"""Full read-only backup of the hackingbiology.com WordPress.com site."""
import io, json, os, re, sys, time
import urllib.request, urllib.error

SITE = "221097453"
API = "https://public-api.wordpress.com/rest/v1.1/sites/%s/" % SITE
STAMP = sys.argv[1] if len(sys.argv) > 1 else "latest"
# Backups live OUTSIDE the repo: they contain unpublished drafts and the admin email.
OUT = os.path.join(os.path.expanduser("~"), "hackingbiology-refs", "site-backup-" + STAMP)
TOK = json.load(io.open(r"C:\Users\admin\.hackingbiology\token.json", encoding="utf-8"))["access_token"]


def get(path, binary=False):
    url = path if path.startswith("http") else API + path
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOK,
                                               "User-Agent": "hb-backup/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            return data if binary else json.loads(data.decode("utf-8"))
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2)


def save_json(name, obj):
    p = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(
        json.dumps(obj, ensure_ascii=False, indent=2))
    return p


def fetch_all(kind):
    """Paginate through posts/pages of every status."""
    items, page, seen = [], 1, set()
    while True:
        d = get("posts/?type=%s&status=any&number=20&page=%d&context=edit" % (kind, page))
        batch = d.get("posts", [])
        new = [p for p in batch if p["ID"] not in seen]
        for p in new:
            seen.add(p["ID"])
        items += new
        if not new or len(items) >= d.get("found", 0):
            break
        page += 1
    return items


def slugify(p):
    s = p.get("slug") or re.sub(r"[^a-z0-9]+", "-", (p.get("title") or "untitled").lower()).strip("-")
    return (s or "untitled")[:60]


os.makedirs(OUT, exist_ok=True)
report = {}

# --- site-level metadata ---
for name, path in [("site.json", ""), ("settings.json", "settings"),
                   ("theme.json", "themes/mine"), ("categories.json", "categories/?number=100"),
                   ("tags.json", "tags/?number=200"), ("menus.json", "menus"),
                   ("users.json", "users")]:
    try:
        save_json("meta/" + name, get(path))
    except Exception as e:
        print("  ! meta/%s failed: %s" % (name, e))

# --- posts + pages ---
for kind in ("post", "page"):
    items = fetch_all(kind)
    save_json("%ss.json" % kind, items)
    report[kind] = {"total": len(items),
                    "publish": sum(1 for p in items if p["status"] == "publish"),
                    "draft": sum(1 for p in items if p["status"] == "draft"),
                    "other": sum(1 for p in items if p["status"] not in ("publish", "draft"))}
    for p in items:
        fn = "content/%ss/%s-%s-%s.html" % (kind, p["status"], p["ID"], slugify(p))
        body = u"<!-- ID:%s status:%s date:%s slug:%s url:%s -->\n<h1>%s</h1>\n%s" % (
            p["ID"], p["status"], p.get("date"), p.get("slug"), p.get("URL"),
            p.get("title") or "", p.get("content") or "")
        pth = os.path.join(OUT, fn)
        os.makedirs(os.path.dirname(pth), exist_ok=True)
        io.open(pth, "w", encoding="utf-8", newline="\n").write(body)
    print("  %ss: %s" % (kind, report[kind]))

# --- media (metadata + binaries) ---
media, page = [], 1
while True:
    d = get("media/?number=100&page=%d" % page)
    batch = d.get("media", [])
    media += batch
    if len(media) >= d.get("found", 0) or not batch:
        break
    page += 1
save_json("media.json", media)

ok = failed = 0
for m in media:
    url = m.get("URL")
    if not url:
        continue
    fn = os.path.basename(url.split("?")[0]) or ("media-%s" % m["ID"])
    pth = os.path.join(OUT, "media", "%s-%s" % (m["ID"], fn))
    os.makedirs(os.path.dirname(pth), exist_ok=True)
    if os.path.exists(pth) and os.path.getsize(pth) > 0:
        ok += 1
        continue
    try:
        io.open(pth, "wb").write(get(url, binary=True))
        ok += 1
    except Exception as e:
        failed += 1
        print("  ! media %s (%s) failed: %s" % (m["ID"], fn, e))
report["media"] = {"total": len(media), "downloaded": ok, "failed": failed}
print("  media: %s" % report["media"])

save_json("MANIFEST.json", {"site_id": SITE, "domain": "hackingbiology.com",
                            "taken": "2026-08-18", "counts": report,
                            "note": "Read-only backup via WordPress.com REST v1.1 (context=edit)."})
print("\nBackup dir:", OUT)
