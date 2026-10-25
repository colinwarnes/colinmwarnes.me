"""Build publications.json from an ORCID record.

Works come from the ORCID public API; authors and venue are filled in from
Crossref using each work's DOI. Standard library only. If ORCID can't be
reached the script exits non-zero and leaves publications.json untouched.
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ORCID_ID = "0000-0003-3088-8429"
OUT = Path(__file__).resolve().parent.parent / "publications.json"
PROFILE_URL = f"https://orcid.org/{ORCID_ID}"
USER_AGENT = "colinmwarnes.me publications updater (https://colinmwarnes.me)"


def get_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def clean(text):
    return re.sub(r"<[^>]+>", "", text or "").strip().rstrip(".")


def crossref(doi):
    try:
        return get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
    except Exception as e:
        print(f"warning: Crossref lookup failed for {doi}: {e}", file=sys.stderr)
        return {}


def main():
    works = get_json(f"https://pub.orcid.org/v3.0/{ORCID_ID}/works")["group"]

    pubs = []
    for group in works:
        s = group["work-summary"][0]
        ids = s.get("external-ids") or {}
        doi = next((e["external-id-value"] for e in ids.get("external-id", [])
                    if e["external-id-type"] == "doi"), None)
        year = ((s.get("publication-date") or {}).get("year") or {}).get("value")
        cr = crossref(doi) if doi else {}

        authors = ", ".join(" ".join(filter(None, [a.get("given"), a.get("family")]))
                            for a in cr.get("author", []))
        preprint = s.get("type") == "preprint"
        venue = (cr.get("container-title") or [None])[0] or (s.get("journal-title") or {}).get("value")
        if preprint and not venue:
            venue = (cr.get("institution") or [{}])[0].get("name") or "Preprint"

        pubs.append({
            "title": clean((cr.get("title") or [None])[0] or s["title"]["title"]["value"]),
            "authors": authors,
            "venue": venue or "",
            "year": int(year) if year else None,
            "preprint": preprint,
            "url": f"https://doi.org/{doi}" if doi else (s.get("url") or {}).get("value"),
        })

    if not pubs:
        sys.exit("No works returned; leaving publications.json unchanged.")

    pubs.sort(key=lambda p: p["year"] or 0, reverse=True)
    data = {"updated": date.today().isoformat(), "profile": PROFILE_URL, "publications": pubs}
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(pubs)} publications to {OUT}")


if __name__ == "__main__":
    main()
