"""Verify permanent resources and compare all unrelated Hugo output bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


def html_ids(text):
    """Read semantic IDs even when Hugo minification removes attribute quotes."""
    class Parser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.ids = set()
        def handle_starttag(self, tag, attrs):
            value = dict(attrs).get('id')
            if value is not None: self.ids.add(value)
    parser = Parser()
    parser.feed(text)
    return parser.ids


def check(public, baseline=None):
    for name in ("index.html", "cv/index.html", "cv/en/index.html", "cv.json", "profile.json", "ryan.vcf"):
        if not (public / "about" / name).is_file():
            raise ValueError(f"Missing /about/{name}")
    cv = json.loads((public / "about/cv.json").read_text(encoding="utf-8"))
    for group in ("entries", "works", "media"):
        if any(x.get("visibility") == "private" or x.get("status") in {"draft", "cancelled"} for x in cv[group]):
            raise ValueError("Nonpublic record leaked to cv.json")
    for path in public.rglob("index.xml"):
        if "/about/cv/" in path.read_text(encoding="utf-8"):
            raise ValueError(f"CV leaked into RSS: {path}")
    for path in (public / "index.html", *public.glob("page/*/index.html"), *public.glob("arts/**/index.html"), *public.glob("refs/**/index.html"), *public.glob("techs/**/index.html"), *public.glob("etcs/**/index.html")):
        if "/about/cv/" in path.read_text(encoding="utf-8"):
            raise ValueError(f"CV leaked into blog listing: {path}")
    for lang in ("ko", "en"):
        path = public / ("about/cv/index.html" if lang == "ko" else "about/cv/en/index.html")
        text = path.read_text(encoding="utf-8")
        if not {"writings", "press"} <= html_ids(text):
            raise ValueError("Required CV anchor missing")
    for item in cv["works"]:
        if item.get("archive_url", "").startswith("/"):
            path = public / urllib.parse.unquote(item["archive_url"]).strip("/") / "index.html"
            if not path.exists():
                raise ValueError(f"Archive permalink does not exist: {item['id']}")
    vcard = (public / "about/ryan.vcf").read_text(encoding="utf-8")
    if "VERSION:4.0" not in vcard or "TEL:" in vcard or "ADR:" in vcard:
        raise ValueError("Invalid public vCard")
    robots = (public / "robots.txt").read_text(encoding="utf-8")
    if "Allow: /about/" not in robots or "Disallow: /about/" in robots:
        raise ValueError("About crawling is not allowed")
    if (public / "about/cv/_print").exists():
        raise ValueError("Intermediate print pages must not be deployed")
    differences = []
    if baseline:
        paths = {p.relative_to(baseline).as_posix() for p in baseline.rglob("*") if p.is_file()} | {p.relative_to(public).as_posix() for p in public.rglob("*") if p.is_file()}
        for name in sorted(paths):
            # Sitemap additions and the explicit robots allow rule are required.
            if name.startswith("about/") or name == "robots.txt" or name.endswith("sitemap.xml"):
                continue
            before, after = baseline / name, public / name
            if not before.is_file() or not after.is_file() or before.read_bytes() != after.read_bytes():
                differences.append(name)
        if differences:
            raise ValueError("Unrelated output changed:\n" + "\n".join(differences))
    return {"public_entries": len(cv["entries"]), "public_works": len(cv["works"]), "public_media": len(cv["media"]), "unrelated_differences": differences}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--public", type=Path, default=Path("public"))
    p.add_argument("--baseline", type=Path)
    args = p.parse_args()
    print(json.dumps(check(args.public, args.baseline), ensure_ascii=False))
