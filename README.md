# colinmwarnes.me

Personal site for Colin M. Warnes. Plain HTML/CSS served by GitHub Pages.

Edit `index.html` (content) and `style.css` (look), then commit and push to `main`.

## Publications

The publications list is rendered from `publications.json`, which the
**Update publications** GitHub Action refreshes every Monday from the
ORCID record (`scripts/update_publications.py`; authors and venues come from Crossref).
Run it manually from the repo's **Actions** tab ("Run workflow"). If ORCID
is unreachable, the previous list stays in place.
