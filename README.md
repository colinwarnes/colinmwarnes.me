# colinmwarnes.me

Personal site for Colin M. Warnes. Plain HTML/CSS served by GitHub Pages.

Edit `index.html` (content) and `style.css` (look), then commit and push to `main`.

## Publications

The publications list is rendered from `publications.json`, which the
**Update publications** GitHub Action refreshes every Monday by scraping the
Google Scholar profile (`scripts/update_publications.py`, using `scholarly`).
Run it manually from the repo's **Actions** tab ("Run workflow"). If Scholar
blocks the run, the previous list stays in place.
