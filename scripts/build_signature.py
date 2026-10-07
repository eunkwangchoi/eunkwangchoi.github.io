"""Generate local-only HTML/plain-text email signatures from public profile data."""
import argparse
import html
from pathlib import Path
from urllib.parse import urljoin
import yaml

ROOT = Path(__file__).resolve().parents[1]


def build(destination=ROOT / "dist-local/signature"):
    destination.mkdir(parents=True, exist_ok=True)
    profile = yaml.safe_load((ROOT / "data/me/profile.yaml").read_text(encoding="utf-8"))
    links = yaml.safe_load((ROOT / "data/me/links.yaml").read_text(encoding="utf-8"))
    base = profile["url"]
    previews = []
    for variant in profile["signatures"]:
        selected = [x for x in links if x.get("signature") and x["label"] in variant["labels"]]
        for lang in ("ko", "en"):
            name = profile["name"]["ko"] if lang == "ko" else profile["name"]["full_en"]
            title = variant["title"][lang]
            plain = f"{name}\n{title}\n{profile['email']}\n{base}\n" + "\n".join(f"{x['title']}: {urljoin(base, x['url'])}" for x in selected)
            avatar = ""
            if profile.get("avatar"):
                avatar = f'<td style="vertical-align:top;padding:0 16px 0 0"><img src="{urljoin(base, "/about/avatar/128.jpg")}" alt="{html.escape(name)}" width="64" height="64" style="display:block;border:0;background:#ffffff"></td>'
            link_row = ' · '.join(f'<a href="{html.escape(urljoin(base, x["url"]), quote=True)}" style="color:#b02a37;text-decoration:underline">{html.escape(x["title"])}</a>' for x in selected)
            markup = f'<table role="presentation" cellpadding="0" cellspacing="0" style="border-collapse:collapse;background:#ffffff;color:#212529"><tr>{avatar}<td style="vertical-align:top;padding:0;font:13px/20px Arial,sans-serif"><strong style="font:700 18px/24px Georgia,serif">{html.escape(name)}</strong><br>{html.escape(title)}<br><a href="mailto:{html.escape(profile["email"])}" style="color:#b02a37">{html.escape(profile["email"])}</a><br><a href="{html.escape(base)}" style="color:#b02a37">{html.escape(base)}</a><br>{link_row}</td></tr></table>'
            if len(markup) > 10000:
                raise ValueError("Signature exceeds 10,000 characters")
            stem = f"{variant['id']}-{lang}"
            (destination / f"{stem}.html").write_text(markup, encoding="utf-8")
            (destination / f"{stem}.txt").write_text(plain, encoding="utf-8")
            previews.append(f'<section><h2>{stem}</h2><div id="{stem}" data-signature>{markup}</div><button type="button" data-copy="{stem}">Copy HTML + text</button><a href="{stem}.txt">Text</a></section>')
    preview = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="robots" content="noindex"><title>Email signatures</title><style>body{max-width:50em;margin:32px auto;padding:16px;font-family:Arial,sans-serif}section{margin:32px 0}button,a{margin:16px 16px 16px 0}#status{min-height:24px}</style><h1>Email signatures</h1><p>Copy the rendered signature into Gmail settings.</p><p id="status" role="status"></p>''' + ''.join(previews) + '''<script>
document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{
 const box=document.getElementById(button.dataset.copy);
 try{await navigator.clipboard.write([new ClipboardItem({'text/html':new Blob([box.innerHTML],{type:'text/html'}),'text/plain':new Blob([box.innerText],{type:'text/plain'})})]);document.getElementById('status').textContent='Copied.';}
 catch{const range=document.createRange();range.selectNodeContents(box);const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);document.getElementById('status').textContent='Signature selected. Press Ctrl+C or use your browser Copy command.';}
}));</script></html>'''
    (destination / "index.html").write_text(preview, encoding="utf-8")
    print(f"Generated {len(previews)} local signature variants: {destination}")


if __name__ == "__main__":
    build()
