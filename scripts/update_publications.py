"""Fetch publications from a Google Scholar profile and write publications.json.

Google Scholar has no official API, so this uses the `scholarly` scraper.
If Scholar blocks the request, the script exits non-zero and leaves the
existing publications.json untouched.
"""

import json
import sys
from datetime import date
from pathlib import Path

from scholarly import scholarly

SCHOLAR_ID = "NMVFXaMAAAAJ"
OUT = Path(__file__).resolve().parent.parent / "publications.json"
PROFILE_URL = f"https://scholar.google.com/citations?user={SCHOLAR_ID}"


def format_authors(raw):
    names = [n.strip() for n in raw.split(" and ") if n.strip()]
    return ", ".join(names)


def main():
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=["basics", "indices", "publications"])

    pubs = []
    for pub in author.get("publications", []):
        try:
            pub = scholarly.fill(pub)
        except Exception as e:  # keep the summary data if the detail page fails
            print(f"warning: could not fill '{pub['bib'].get('title')}': {e}", file=sys.stderr)
        bib = pub.get("bib", {})
        venue = bib.get("journal") or bib.get("conference") or bib.get("publisher") or bib.get("citation", "")
        pubs.append({
            "title": bib.get("title", ""),
            "authors": format_authors(bib.get("author", "")),
            "venue": venue,
            "year": int(bib["pub_year"]) if str(bib.get("pub_year", "")).isdigit() else None,
            "citations": pub.get("num_citations", 0),
            "url": pub.get("pub_url")
                   or f"https://scholar.google.com/citations?view_op=view_citation&citation_for_view={pub.get('author_pub_id', '')}",
        })

    if not pubs:
        sys.exit("No publications returned; leaving publications.json unchanged.")

    pubs.sort(key=lambda p: (p["year"] or 0, p["citations"]), reverse=True)
    data = {
        "updated": date.today().isoformat(),
        "profile": PROFILE_URL,
        "total_citations": author.get("citedby"),
        "h_index": author.get("hindex"),
        "publications": pubs,
    }
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(pubs)} publications to {OUT}")


if __name__ == "__main__":
    main()
