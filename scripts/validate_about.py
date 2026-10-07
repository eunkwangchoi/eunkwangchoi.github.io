"""Validate public CV data, front matter, vocabulary and reference integrity."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import sys
import tomllib

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def front_matter(path):
    text = path.read_text(encoding="utf-8-sig")
    if text.startswith("+++"):
        return tomllib.loads(text.split("+++", 2)[1])
    if text.startswith("---"):
        return yaml.safe_load(text.split("---", 2)[1]) or {}
    return {}


def records(root=ROOT):
    result = []
    for folder, definition in (("entries", "entry"), ("works", "work")):
        for p in (root / "data/cv" / folder).glob("*.yaml"):
            result.extend((p, definition, x) for x in load(p))
    for filename, definition in (("media", "media"), ("orgs", "org"), ("series", "series")):
        p = root / f"data/cv/{filename}.yaml"
        result.extend((p, definition, x) for x in load(p))
    config = tomllib.loads((root / "hugo.toml").read_text(encoding="utf-8"))
    content = root / config.get("contentDir", "content")
    for base in {content, root / "content"}:
        for p in base.rglob("*.md"):
            meta = front_matter(p)
            if meta.get("cv"):
                item = dict(meta["cv"])
                item.setdefault("id", "archive-" + hashlib.sha256(p.relative_to(base).as_posix().encode()).hexdigest()[:16])
                result.append((p, "frontmatter", item))
    return result


def validate(root=ROOT):
    schema = json.loads((root / "schema/cv.schema.json").read_text(encoding="utf-8"))
    vocab = load(root / "data/cv/vocab.yaml")
    errors = []
    def check(value, definition, origin):
        # JSON Schema treats serialized YAML dates as ISO strings.
        serial = json.loads(json.dumps(value, default=str))
        validator = jsonschema.Draft202012Validator({"$ref": f"#/$defs/{definition}", "$defs": schema["$defs"]})
        for e in validator.iter_errors(serial):
            errors.append(f"{origin}: {'/'.join(map(str, e.path))}: {e.message}")
    check(load(root / "data/me/profile.yaml"), "profile", "profile")
    links = load(root / "data/me/links.yaml")
    for x in links:
        check(x, "hubLink", x.get("id", "link"))
    featured = sorted([x for x in links if x.get("type") == "featured"], key=lambda x: x.get("order", 0))
    if not 1 <= len(featured) <= 7 or featured[0]["id"] != "cv":
        errors.append("Featured links must number 1-7, with CV first.")
    check(load(root / "data/me/tokens.yaml"), "tokens", "tokens")
    fonts = load(root / "data/me/fonts.yaml")
    if fonts.get("mode") not in {"local", "web"} or not isinstance(fonts.get("web_pdf_permitted"), bool):
        errors.append("Invalid PDF font configuration")
    for role, font in fonts.get("roles", {}).items():
        if not isinstance(font.get("family"), str) or font.get("style") not in {"normal", "italic"} or font.get("weight") not in range(100, 1000, 100):
            errors.append(f"Invalid PDF font role: {role}")
    palette = load(root / "data/me/pdf_tokens.yaml")
    for role, colors in palette.items():
        for color in (colors.values() if isinstance(colors, dict) else [colors]):
            if not isinstance(color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
                errors.append(f"Invalid PDF color: {role}")
    check(vocab, "vocab", "vocab")
    items = records(root)
    ids = {}
    for p, definition, item in items:
        check(item, definition, p.relative_to(root))
        if item.get("visibility") != "private" and item.get("status") not in {"draft", "cancelled"}:
            localized = item.get("name" if definition == "org" else "title", {})
            english = item.get("title_en") if definition == "frontmatter" else localized.get("en")
            if not english:
                errors.append(f"{item['id']}: missing English title/name")
            if item.get("details") and not item.get("details_en"):
                errors.append(f"{item['id']}: missing English details")
            if item.get("description") and not item["description"].get("en"):
                errors.append(f"{item['id']}: missing English description")
        if item["id"] in ids:
            errors.append(f"Duplicate id: {item['id']}")
        ids[item["id"]] = definition
        for key, allowed in (("domain", vocab["domains"]), ("kind", vocab["kinds"])):
            if key in item and item[key] not in allowed:
                errors.append(f"{item['id']}: unknown {key}: {item[key]}")
        if "type" in item:
            allowed = vocab["media_types"] if definition == "media" else vocab["work_types"]
            if item["type"] not in allowed:
                errors.append(f"{item['id']}: unknown type: {item['type']}")
    expected = {"works": {"work", "frontmatter"}, "media": {"media"}, "about": {"entry", "work", "frontmatter"}, "org": {"org"}, "publisher": {"org"}, "outlet": {"org"}, "venue": {"org", "series"}, "series": {"series"}}
    for p, definition, item in items:
        for field, kinds in expected.items():
            values = item.get(field) or []
            if isinstance(values, str):
                values = [values]
            for ref in values:
                if ids.get(ref) not in kinds:
                    errors.append(f"{item['id']}: missing or invalid {field} reference {ref}")
        # Reject identifiers even when a record is private: this repo is public.
        for key in ("phone", "address", "student_id", "member_id", "certificate_id", "military_id", "private_overlay"):
            if key in item:
                errors.append(f"{item['id']}: private field {key} forbidden in public source")
        for key in ("title", "description", "details", "details_en"):
            text = json.dumps(item.get(key, ""), ensure_ascii=False)
            if re.search(r"\b(?:\d{10,}|[A-Z]{2,}-\d{4,}|\d{2}-\d{2}-\d{4,}|\d{8}-\d{8,}-\d+|\d{2}-[A-Z]\d-\d{6,})\b", text):
                errors.append(f"{item['id']}: possible private identifier in {key}")
    for book in load(root / "data/me/books.yaml"):
        check(book, "bookCover", book.get("id", "cover"))
        if ids.get(book["id"]) not in {"work", "frontmatter"}:
            errors.append(f"Unknown book cover reference: {book['id']}")
        if not (root / "assets" / book["cover"]).is_file():
            errors.append(f"Missing cover: {book['cover']}")
    if errors:
        raise ValueError("\n".join(errors))
    return len(items)


if __name__ == "__main__":
    try:
        print(f"Validated {validate()} CV records and hub data.")
    except (ValueError, KeyError) as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
