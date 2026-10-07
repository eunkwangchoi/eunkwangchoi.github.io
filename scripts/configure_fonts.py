"""Read existing Adobe kits with a locally supplied token; save public CSS mappings.

The token is read from ADOBE_FONTS_TOKEN or an interactive, hidden prompt. It is
never printed or saved. This command does not create/publish/delete Adobe kits.
"""
import argparse
import getpass
import json
import os
from pathlib import Path
import urllib.request
import yaml
from validate_about import ROOT


def request(path, token):
    req = urllib.request.Request("https://typekit.com/api/v1/json/" + path, headers={"X-Typekit-Token": token})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def configure(kit, token):
    result = request("kits/" + kit, token)["kit"]
    fonts = yaml.safe_load((ROOT / "data/me/fonts.yaml").read_text(encoding="utf-8"))
    matched = set()
    for family in result["families"]:
        names = family.get("css_names") or [family.get("slug", "")]
        name = names[0]
        slug = (family.get("name", "") + " " + name).lower()
        for role, font in fonts["roles"].items():
            match = ((role == "display" and "eaves" in slug and ("mod" in slug or "modern" in slug)) or (role in {"contact", "label_en"} and "eaves" in slug and "san" in slug) or (role in {"light", "body_en", "italic_en", "strong_en", "strong_italic_en", "date_en"} and "frank" in slug))
            if not match:
                continue
            variations = family.get("variations", [])
            variation = ("i" if font["style"] == "italic" else "n") + str(font["weight"] // 100)
            if variations and variation not in variations:
                raise ValueError(f"Kit lacks required variation {variation} for {role}. Inspect the actual kit style mapping.")
            font["family"] = name
            font["source"] = "web"
            matched.add(role)
    required = {"display", "contact", "light", "label_en", "body_en", "italic_en", "strong_en", "strong_italic_en", "date_en"}
    if matched != required:
        raise ValueError("Kit lacks required Adobe font families.")
    for role, font in fonts["roles"].items():
        if role not in matched:
            font["source"] = "local"
    fonts["mode"] = "web"
    fonts["kit"] = f"https://use.typekit.net/{kit}.css"
    # Web PDF permission is a separate explicit setting; API entitlement is not it.
    (ROOT / "data/me/fonts.yaml").write_text(yaml.safe_dump(fonts, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Saved public CSS URL and {len(matched)} Adobe role mappings. Korean local fonts preserved; PDF permission setting unchanged.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--kit", help="Existing public kit id")
    p.add_argument("--local", action="store_true", help="Use local PostScript names through explicit @font-face aliases")
    p.add_argument("--token-file", type=Path, help="Read a token from a local ignored file; never print or save it")
    args = p.parse_args()
    if args.local:
        path = ROOT / "data/me/fonts.yaml"
        fonts = yaml.safe_load(path.read_text(encoding="utf-8"))
        fonts["mode"] = "local"
        for role, font in fonts["roles"].items():
            font["family"] = "CV-" + role.replace("_", "-")
            font["source"] = "local"
        path.write_text(yaml.safe_dump(fonts, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print("Configured local aliases. PDF build still verifies actual font loading.")
    else:
        token = (args.token_file.read_text(encoding="utf-8-sig").strip() if args.token_file else os.environ.get("ADOBE_FONTS_TOKEN")) or getpass.getpass("Adobe Fonts token (not saved): ")
        try:
            if args.kit:
                configure(args.kit, token)
            else:
                result = request("kits", token)
                print(json.dumps({"kits": result.get("kits", [])}, ensure_ascii=False, indent=2))
        except Exception as error:
            raise SystemExit(f"Adobe API request failed: {type(error).__name__}. No token is included in this diagnostic.")
