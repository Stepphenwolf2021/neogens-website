# Neo Gens — Company Website

Site for **Neo Gens**, a Modern Knowledge Management practice. First practice area:
museums, libraries and archives.

- Live site: https://www.neogens.co
- Stack: static HTML (no build step, no external CSS/JS — each page is self-contained)
- Languages: English (no prefix) and Thai (`th-` prefix), page for page

## Structure

Multi-page. Each section of the old single-page site is now its own page, and the
English and Thai trees mirror each other exactly.

| File | Page |
|------|------|
| `index.html` / `th-index.html` | Home — hero plus a directory of every section |
| `problem.html` / `th-problem.html` | The problem |
| `what.html` / `th-what.html` | What Modern KM is |
| `why.html` / `th-why.html` | Why it works |
| `visit.html` / `th-visit.html` | KM for Museums & Libraries · 01 — where it stands today |
| `experience.html` / `th-experience.html` | 02 — visitors and readers |
| `museums.html` / `th-museums.html` | 03 — what leadership looks like |
| `services.html` / `th-services.html` | What we do together |
| `engagement.html` / `th-engagement.html` | Engagement |
| `proof.html` / `th-proof.html` | Reference implementation |
| `honest.html` / `th-honest.html` | What we won't do |
| `contact.html` / `th-contact.html` | Request a briefing |
| `km-for-museums-and-libraries.html` | Long read (EN) |
| `km-for-museums.html` | Redirect stub for the old long-read URL |
| `404.html` | Not found |
| `sitemap.xml`, `robots.txt` | Crawling |
| `favicon.svg`, `logo.svg`, `logo-light.svg`, `og-image.png` | Brand assets |
| `archive/` | Superseded pages. `noindex`, not in the sitemap, never link here from the live site |

Each HTML file carries its own CSS and JS inline, so there is no shared stylesheet to
keep in sync. Diagrams are hand-authored inline SVG.

## Conventions worth knowing before editing

- **Edit both languages in the same pass.** Doing one and deferring the other is how
  fourteen meaning drifts got into v1. `.tools/check.py` compares the two trees
  page by page and fails if a block exists on one side only.
- **Colours are tokens, never literals.** Everything resolves through CSS custom
  properties, including inline SVG `fill`/`stroke` and every `rgba()` (`--go-rgb`,
  `--w-rgb`, …). A hardcoded hex will look correct in dark mode and wrong in light.
- **Thai never takes negative `letter-spacing`,** and `line-height` stays at or above
  1.3, or the tone marks collide. Latin-only rules (`.brand .bt`, `.en`, mono labels)
  are the exception.
- **No statistics that cannot be sourced.** The site deliberately carries no
  performance figures. The checker flags any that appear.
- **Old anchors still resolve.** `index.html` and `th-index.html` read `#section`
  from the URL and forward to the matching page, so links shared before the split
  keep working. Keep that script if you rewrite the home page.

## Publishing

Double-click, in this order:

1. `check.command` — structure, dead links, duplicate ids and canonicals, Thai
   diacritic order, unverifiable figures, EN↔TH parity
2. `publish.command` — pulls, re-checks, shows you the diff, asks before pushing

Both are local-only (git-ignored). The logic lives in `.tools/`, which is committed
but never served, because GitHub Pages skips dot-directories.

The checker does **not** tell you whether the page looks right, or whether the English
and Thai still say the same thing. Open the files in a browser first — both themes,
and a narrow window as well as a wide one.

## Hosting

GitHub Pages from the repository root. Custom domain in `CNAME`.
