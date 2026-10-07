"""Reconcile a Raindrop API/export JSON into a reviewable, local migration plan.

No account deletion and no automatic content edits. API reads use an environment
token, never a command argument. Apply approved records at their sole source.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import urllib.request
from validate_about import ROOT, front_matter


def normalize(title):
    return re.sub(r"[^\w]", "", title.casefold())


def fetch(collection):
    token = os.environ.get("RAINDROP_TOKEN")
    if not token:
        raise ValueError("Set RAINDROP_TOKEN locally, or use --export with a JSON export.")
    items = []
    for page in range(100):
        request = urllib.request.Request(f"https://api.raindrop.io/rest/v1/raindrops/{collection}?perpage=50&page={page}", headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(request, timeout=30) as response:
            batch = json.load(response)
        if not batch.get("result"):
            raise ValueError("Raindrop API rejected request")
        items.extend(batch["items"])
        if len(batch["items"]) < 50:
            return items
    raise ValueError("Pagination limit exceeded; export incomplete")


def reconcile(items, collection):
    archive = []
    for p in (ROOT / "themes/write-only/content").rglob("*.md"):
        meta = front_matter(p)
        archive.append((p.relative_to(ROOT).as_posix(), meta))
    result = []
    for item in items:
        title, url = item.get("title", ""), item.get("link", "")
        candidates = [path for path, meta in archive if (url and url == meta.get("cv", {}).get("original_url")) or normalize(title) == normalize(meta.get("title", ""))]
        note = item.get("note", "") or item.get("excerpt", "")
        match = re.search(r"(\d{4})[.\-/]\s*(\d{1,2})(?:[.\-/]\s*(\d{1,2}))?", note)
        date = "-".join([match[1], match[2].zfill(2)] + ([match[3].zfill(2)] if match[3] else [])) if match else None
        result.append({"raindrop_id": item.get("_id"), "title": title, "original_url": url, "order": item.get("sort"), "tags": item.get("tags", []), "note": note, "created": item.get("created"), "date": date, "precision": "day" if date and len(date) == 10 else "month", "candidates": candidates, "destination": candidates[0] if len(candidates) == 1 and collection == "writings" else ("data/cv/media.yaml" if collection == "press" else "data/cv/works/external.yaml"), "decision": "matched" if len(candidates) == 1 else "review"})
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--collection", choices=["writings", "press"], required=True)
    p.add_argument("--export", type=Path)
    p.add_argument("--api", action="store_true")
    args = p.parse_args()
    if bool(args.export) == args.api:
        p.error("Choose one of --export or --api")
    raw = json.loads(args.export.read_text(encoding="utf-8")) if args.export else fetch(48166830 if args.collection == "writings" else 48167837)
    items = raw.get("items", []) if isinstance(raw, dict) else raw
    expected = 39 if args.collection == "writings" else 12
    if len(items) != expected:
        raise ValueError(f"Expected {expected} collection items, got {len(items)}; no migration applied")
    target = ROOT / "dist-local/migration"
    target.mkdir(parents=True, exist_ok=True)
    (target / f"{args.collection}.json").write_text(json.dumps(reconcile(items, args.collection), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(items)} records for reconciliation. Raindrop account unchanged.")
