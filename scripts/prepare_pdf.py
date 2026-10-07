"""Add an ephemeral Hugo mount for print intermediates; normal builds omit it."""
import json
from pathlib import Path
import tomllib
import yaml
import argparse
from validate_about import ROOT


def prepare(selection=None):
    profile = yaml.safe_load((ROOT / "data/me/profile.yaml").read_text(encoding="utf-8"))
    root = ROOT / ".build/print-content"
    for variant in profile["pdf"]["variants"]:
        for lang in ("ko", "en"):
            path = root / f"about/cv/_print/{variant}-{lang}/index.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"---\ntitle: CV {variant} {lang}\ntype: about\nlayout: cv-print\ncvlang: {lang}\ncvvariant: {variant}\noutputs: [HTML]\nrobots: noindex\nsitemap:\n  disable: true\nparams:\n  noindex: true\n  excludeFromSitemap: true\n  excludeFromLists: true\nbuild:\n  list: never\n---\n", encoding="utf-8")
    config = tomllib.loads((ROOT / "hugo.toml").read_text(encoding="utf-8"))
    mounts = config["module"]["mounts"] + [{"source": ".build/print-content", "target": "content"}]
    if selection:
        from cv_private import print_data
        private_data = ROOT / '.build/private-print-data'
        private_data.mkdir(parents=True, exist_ok=True)
        (private_data / 'cv_private.json').write_text(json.dumps(print_data(selection), ensure_ascii=False, default=str), encoding='utf-8')
        mounts += [{"source": "data", "target": "data"}, {"source": str(private_data), "target": "data"}]
    lines = []
    for mount in mounts:
        lines.append("[[module.mounts]]")
        lines.extend(f"{k} = {json.dumps(v)}" for k,v in mount.items())
    config_path = ROOT / ".build/pdf.toml"
    config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Print-only Hugo config: .build/pdf.toml")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--selection', type=Path)
    prepare(parser.parse_args().selection)
