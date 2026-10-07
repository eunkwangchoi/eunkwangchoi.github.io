"""Export a reviewable English Markdown CV from Hugo's public merged JSON."""
import argparse
import json
from pathlib import Path


def export(source, target):
    cv = json.loads(source.read_text(encoding="utf-8"))
    orgs = cv["orgs"]
    lines = [f"# {cv['profile']['name']['full_en']}", "", "Curriculum Vitae", "",
             cv["profile"]["about"]["en"], "",
             f"Email: {cv['profile']['email']}  ", f"Website: {cv['profile']['url']}", "",
             "English translations of Korean publication titles do not imply English editions. "
             "Source discrepancies and terminology choices are documented in docs/cv-translation-review.md.", ""]

    def item(record):
        title = record["title"]["en"]
        if record.get("original_language") == "ko":
            title += " (in Korean)"
        url = record.get("archive_url") or next((x["url"] for x in record.get("links", []) if x.get("url")), "")
        lines.append(f"- [{title}]({url})" if url else f"- {title}")
        if record.get("description", {}).get("en"):
            lines.append("  - " + record["description"]["en"])
        else:
            metadata = [str(record["date"])] if record.get("date") else []
            if record.get("period"):
                period = record["period"]
                metadata.append(str(period["start"]) + (" – Present" if period.get("ongoing") else " – " + str(period["end"]) if period.get("end") else ""))
            for field in ("org", "publisher"):
                metadata += [orgs[x]["name"]["en"] for x in record.get(field, [])]
            for field in ("venue", "outlet"):
                if record.get(field):
                    metadata.append(orgs[record[field]]["name"]["en"])
            if record.get("extent_en"):
                metadata.append(record["extent_en"])
            metadata += [f"{k.upper()}: {v}" for k, v in record.get("ids", {}).items() if k in {"isbn", "doi"}]
            if metadata:
                lines.append("  - " + "; ".join(metadata))
        for detail in record.get("details_en", []):
            lines.append("  - " + detail)
        if record.get("advisor_en"):
            lines.append("  - Advisor: " + record["advisor_en"])
        for ref in record.get("works", []):
            work = next(x for x in cv["works"] if x["id"] == ref)
            lines.append("  - " + work["title"]["en"])

    seen = set()
    for section in cv["vocab"]["sections"]["web"]:
        origin = section["source"]
        if origin == "current":
            continue  # The same records appear in their substantive sections below.
        pool = cv["entries"] if origin == "entries" else cv["media"] if origin == "media" else cv["works"]
        field = "kind" if origin == "entries" else "type"
        accepted = section.get("kinds", section.get("types", []))
        selected = [x for x in pool if x.get(field) in accepted]
        if not selected:
            continue
        lines += ["## " + section["title"]["en"], ""]
        for record in sorted(selected, key=lambda x: str(x.get("date", x.get("period", {}).get("start", ""))), reverse=True):
            item(record)
            seen.add(record["id"])
        lines.append("")
    all_ids = {x["id"] for x in cv["entries"] + cv["works"] + cv["media"]}
    if seen != all_ids:
        raise ValueError("Export omitted public records: " + ", ".join(sorted(all_ids - seen)))
    lines += ["## Interests", ""]
    for interest in cv["profile"]["interests"]:
        lines.append("- " + interest["en"])
    lines += ["", "## Languages", ""]
    for language in cv["profile"]["languages"]:
        lines.append(f"- {language['en']} ({language['level']}/6)")
    lines += ["", f"Updated {cv['updated']}", ""]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")
    print(f"Exported {len(seen)} public CV records to {target}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, default=Path(".build/review-site/about/cv.json"))
    p.add_argument("--output", type=Path, default=Path("dist-local/CV-EN.md"))
    args = p.parse_args()
    export(args.source, args.output)
