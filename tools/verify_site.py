#!/usr/bin/env python3
"""Verify the built Stripchate site: SEO tags, canonicals, JSON-LD, internal links, sitemap."""
import json
import os
import posixpath
import re
import html as h

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://maryamkrol444.github.io/Stripchate/"
GSC = "Xuf94fNm4YX5BqNwEQruet7zaJzvWqv65AoTLLchIj8"
SLUGS = ["strip-chat-com", "www-strip-chat", "stripchate", "stripchata", "stripchat-cim",
         "stripchat-clm", "stripchat-c0m", "stripchat-con", "stripchat-fom", "stripchay", "stripchst"]

errors, warnings = [], []
pages = {}
for root, _, files in os.walk(ROOT):
    if ".git" in root or "tools" in root.split(os.sep):
        continue
    for f in files:
        if f.endswith(".html"):
            rel = os.path.relpath(os.path.join(root, f), ROOT)
            pages[rel] = open(os.path.join(root, f), encoding="utf-8").read()

expected = {"index.html": BASE, **{s + "/index.html": BASE + s + "/" for s in SLUGS}}
titles = {}
for rel, doc in sorted(pages.items()):
    t = re.findall(r"<title>(.*?)</title>", doc, re.S)
    if len(t) != 1:
        errors.append(f"{rel}: {len(t)} <title> tags"); continue
    titles[rel] = h.unescape(t[0]).strip()
    if any(v == titles[rel] and k != rel for k, v in titles.items()):
        errors.append(f"{rel}: duplicate title")
    c = re.findall(r'<link rel="canonical" href="([^"]+)"', doc)
    want = expected.get(rel, BASE)  # 404 canonicals to home
    if len(c) != 1 or c[0] != want:
        errors.append(f"{rel}: canonical {c} != {want}")
    if GSC not in doc:
        errors.append(f"{rel}: missing GSC verification tag")
    if re.search(r"noindex", doc, re.I):
        errors.append(f"{rel}: contains 'noindex'")
    if rel != "404.html" and 'content="index, follow' not in doc:
        errors.append(f"{rel}: missing explicit index,follow robots meta")
    if rel != "404.html":
        if "y9LX8PkDGO4" not in doc:
            errors.append(f"{rel}: missing YouTube video embed")
        if 'property="og:title"' not in doc or 'name="twitter:card"' not in doc:
            errors.append(f"{rel}: missing social meta")
    if "https://striptokens.live/stripchat-com/" not in doc:
        errors.append(f"{rel}: missing CTA link to striptokens.live")
    if 'class="sticky-cta"' not in doc:
        errors.append(f"{rel}: missing sticky CTA bar")
    if len(re.findall(r"<h1[\s>]", doc)) != 1:
        errors.append(f"{rel}: not exactly one <h1>")
    if rel != "404.html" and 'lang="en"' not in doc:
        errors.append(f"{rel}: missing lang attr")
    for i, m in enumerate(re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', doc, re.S)):
        try:
            json.loads(m)
        except Exception as e:
            errors.append(f"{rel}: JSON-LD block {i} invalid: {e}")
    # internal links resolve (relative to the page's directory; absolute allowed only on 404)
    base_dir = posixpath.dirname(rel)
    for href in re.findall(r'<a [^>]*href="([^"]+)"', doc):
        if href.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if href.startswith("/"):
            if rel != "404.html":
                errors.append(f"{rel}: root-absolute internal link {href!r} (breaks on GH Pages subpath)")
            continue
        clean = href.split("#")[0]
        target = posixpath.normpath(posixpath.join(base_dir, clean)) if clean else base_dir
        if target.endswith("/") or clean.endswith("/"):
            target = posixpath.join(target, "index.html") if clean else posixpath.join(base_dir, "index.html")
        if not os.path.exists(os.path.join(ROOT, target)):
            errors.append(f"{rel}: broken link {href!r} -> {target}")

sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = set(re.findall(r"<loc>(.*?)</loc>", sm))
if locs != set(expected.values()):
    errors.append(f"sitemap mismatch: missing={set(expected.values())-locs} extra={locs-set(expected.values())}")
rob = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read()
if "Sitemap:" not in rob:
    errors.append("robots.txt: no Sitemap reference")
if "Disallow" in rob:
    errors.append("robots.txt: unexpected Disallow")

print(f"pages checked: {len(pages)}")
for k, v in sorted(titles.items()):
    print(f"  {v[:82]:84s} <- {k}")
print(f"\nERRORS: {len(errors)}")
for e in errors:
    print("  -", e)
print(f"WARNINGS: {len(warnings)}")
for w in warnings:
    print("  -", w)
raise SystemExit(1 if errors else 0)
