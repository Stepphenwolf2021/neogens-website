# Neo Gens — Company Website

Site for **Neo Gens**, a Modern Knowledge Management practice. First practice area:
museums, libraries and archives.

- Live site: https://www.neogens.co
- Stack: static HTML (no build step, no external CSS/JS — each page is self-contained)
- Languages: English (`index.html`) and Thai (`th-index.html`)

## Structure
| File | Page |
|------|------|
| `index.html` | Home — English |
| `th-index.html` | Home — Thai |
| `km-for-museums.html` | Long read: Modern Knowledge Management for Museums (EN) |
| `404.html` | Not found |
| `sitemap.xml`, `robots.txt` | Crawling |
| `favicon.svg`, `logo.svg`, `logo-light.svg`, `og-image.png` | Brand assets |

Each HTML file carries its own CSS and JS inline, so there is no shared stylesheet to
keep in sync. Diagrams are hand-authored inline SVG.

## Hosting
GitHub Pages from the repository root. Custom domain in `CNAME`.
