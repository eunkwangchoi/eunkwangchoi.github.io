"""Check original media links and request public archives only with --save.

Results are local review proposals. Full article copies never enter this repo.
"""
import argparse
from difflib import SequenceMatcher
import html
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import yaml
from validate_about import ROOT


def inspect(link, expected_title=""):
    request = urllib.request.Request(link["url"], headers={"User-Agent": "CVLinkChecker/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            raw = response.read(1024 * 1024).decode(response.headers.get_content_charset() or "utf-8", errors="replace")
            final_url = response.geturl()
        match = re.search(r"<title[^>]*>(.*?)</title>", raw, re.I | re.S)
        title = html.unescape(re.sub(r"\s+", " ", match[1]).strip()) if match else ""
        homepage = urllib.parse.urlparse(final_url).path in {"", "/"} and urllib.parse.urlparse(link["url"]).path not in {"", "/"}
        soft404 = bool(expected_title and title and SequenceMatcher(None, expected_title.casefold(), title.casefold()).ratio() < 0.45)
        status = "dead" if homepage or soft404 else ("moved" if final_url != link["url"] else "live")
        return {"status": status, "page_title": title, "moved_url": final_url if status == "moved" else None}
    except Exception as exc:
        # Do not store or print request headers or response body.
        return {"status": "dead", "error": type(exc).__name__}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--save", action="store_true", help="Explicitly request Wayback Save Page Now for links without an archive")
    args = p.parse_args()
    records = yaml.safe_load((ROOT / "data/cv/media.yaml").read_text(encoding="utf-8"))
    results = []
    for item in sorted(records, key=lambda x: not any(l["url"].startswith("http:") for l in x["links"])):
        for link in item["links"]:
            result = {"id": item["id"], "url": link["url"], **inspect(link, item.get("page_title", ""))}
            if args.save and not link.get("archive_url"):
                try:
                    request = urllib.request.Request("https://web.archive.org/save/" + link["url"], method="GET", headers={"User-Agent": "CVLinkChecker/1.0"})
                    with urllib.request.urlopen(request, timeout=30) as response:
                        location = response.headers.get("Content-Location", "")
                    if location:
                        result["archive_url"] = urllib.parse.urljoin("https://web.archive.org", location)
                    else:
                        result["archive_pending"] = True
                except Exception as exc:
                    result["archive_error"] = type(exc).__name__
            results.append(result)
    target = ROOT / "dist-local/media"
    target.mkdir(parents=True, exist_ok=True)
    (target / "check.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Checked {len(results)} links. Review proposals saved locally; public data unchanged.")
