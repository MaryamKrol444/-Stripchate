# Stripchate — StripChat Typos & Misspellings (English SEO site)

Static, fully indexable landing site targeting common misspellings of the
StripChat address:

`strip chat com` · `www strip chat` · `stripchate` · `stripchata` ·
`stripchat cim` · `stripchat clm` · `stripchat c0m` · `stripchat con` ·
`stripchat fom` · `stripchay` · `stripchst`

## Structure

- `index.html` — hub page: every typo in one directory table, why each family
  of typos happens, typo-domain safety guide, FAQ.
- One directory per typo (e.g. `stripchat-cim/index.html`) — unique title,
  meta description, H1, body copy, FAQ and self-canonical per keyword.
- Every page (home + subpages) embeds the intro video
  ([youtu.be/y9LX8PkDGO4](https://youtu.be/y9LX8PkDGO4)) at the very top and
  shows a **sticky CTA bar** (bottom, always visible) linking to
  <https://striptokens.live/stripchat-com/>.
- `404.html` — custom error page (absolute links, canonical → home).
- `sitemap.xml` — 12 canonical indexable URLs.
- `robots.txt` — allows everything, references the sitemap.
- Zero JavaScript — pure static HTML/CSS (fast Core Web Vitals, no
  render-dependent content).

## Publishing / SEO settings

- Host: GitHub Pages project site.
- Canonical base: `https://maryamkrol444.github.io/Stripchate/`
  (home canonicals to itself; every subpage canonicals to itself).
- Google Search Console verification meta tag present on **every** page.
- Structured data (JSON-LD): `WebSite` + `Organization` + `BreadcrumbList` +
  `VideoObject` + `FAQPage` (home); `Article` + `BreadcrumbList` +
  `VideoObject` + `FAQPage` (subpages).

## Rebuilding

```bash
python3 tools/build_site.py   # regenerate all pages
python3 tools/verify_site.py  # SEO/technical checks (canonicals, links, JSON-LD, sitemap)
```
