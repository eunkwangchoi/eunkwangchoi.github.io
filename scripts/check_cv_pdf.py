"""Check text, public scope, embedded font families, page cap, and PDF metadata."""
import argparse
import os
from pathlib import Path
import re
import fitz


def embedded_font_name(doc, font):
    xref = font[0]
    if not xref:
        raise ValueError('Font reference missing')
    if font[2] != 'Type3':
        if not doc.extract_font(xref)[3]:
            raise ValueError('Font program is not embedded')
        return font[3].split('+')[-1]
    # Chromium on Windows serializes local CFF fonts as Type3 glyph programs.
    # These embed outlines in CharProcs rather than a FontFile stream.
    kind, descriptor = doc.xref_get_key(xref, 'FontDescriptor')
    if kind != 'xref': raise ValueError('Type3 font descriptor missing')
    kind, name = doc.xref_get_key(int(descriptor.split()[0]), 'FontName')
    if kind != 'name': raise ValueError('Type3 source font name missing')
    kind, chars = doc.xref_get_key(xref, 'CharProcs')
    if kind == 'xref': chars = doc.xref_object(int(chars.split()[0]))
    elif kind != 'dict': raise ValueError('Embedded Type3 glyph dictionary missing')
    glyphs = re.findall(r'\b(\d+) 0 R', chars)
    if not glyphs or any(not doc.xref_is_stream(int(g)) or not doc.xref_stream(int(g)) for g in glyphs):
        raise ValueError('Embedded Type3 glyph program missing')
    kind, unicode = doc.xref_get_key(xref, 'ToUnicode')
    if kind != 'xref' or not doc.xref_stream(int(unicode.split()[0])):
        raise ValueError('Type3 Unicode text mapping missing')
    return name.lstrip('/').split('+')[-1]


def check(path, lang, variant, expected_pages=None):
    doc = fitz.open(path)
    if expected_pages is not None and len(doc) != expected_pages:
        raise ValueError('PDF page count differs from the paginated layout')
    for i, page in enumerate(doc):
        if not re.search(rf'\b{i+1}\s*/\s*{len(doc)}\b', page.get_text()):
            raise ValueError('Blank, duplicate or incorrectly numbered PDF page')
    text = "\n".join(page.get_text() for page in doc)
    if variant == "summary" and len(doc) > 2:
        raise ValueError("Summary exceeds two pages")
    name = "최 은 광" if lang == "ko" else "EUNKWANG"
    if name not in text or "About me" not in text:
        raise ValueError("Name or first heading failed text extraction")
    if re.search(r"(?<![\d-])(?:(?:\+82[- ]?)?0?1[016789][- ]\d{3,4}[- ]\d{4}|\d{2,3}-\d{3,4}-\d{4})(?![\d-])|Penthouse|Neungdong-ro|Gwangjin-gu|\d{1,3}동\s*\d{1,4}호", text, re.I):
        raise ValueError("Possible private phone or address in public PDF")
    fonts = {embedded_font_name(doc, font) for page in doc for font in page.get_fonts()}
    allowed = ("MrEaves", "NewFrank", "KoPubWorldBatang", "NanumGothic")
    if any(not font.startswith(allowed) for font in fonts):
        raise ValueError("Unexpected substitute font: " + ", ".join(sorted(fonts)))
    required = ("MrEaves", "NewFrank") if lang == "en" else ("MrEaves", "NewFrank", "KoPubWorldBatang", "NanumGothic")
    if any(not any(font.startswith(family) for font in fonts) for family in required):
        raise ValueError("Required font family missing: " + ", ".join(sorted(fonts)))
    return doc


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("path", type=Path)
    p.add_argument("--lang", choices=["ko", "en"], required=True)
    p.add_argument("--variant", required=True)
    p.add_argument("--final", type=Path)
    p.add_argument("--expected-pages", type=int)
    args = p.parse_args()
    doc = check(args.path, args.lang, args.variant, args.expected_pages)
    if args.final:
        doc.set_metadata({**doc.metadata, "title": f"Eunkwang Ryan Choi | CV {args.variant} {args.lang}", "author": "Eunkwang Ryan Choi"})
        doc.xref_set_key(doc.pdf_catalog(), "Lang", "(ko-KR)" if args.lang == "ko" else "(en-US)")
        args.final.parent.mkdir(parents=True, exist_ok=True)
        staged = args.final.with_suffix(".pending.pdf")
        doc.save(staged)
        doc.close()
        check(staged, args.lang, args.variant, args.expected_pages).close()
        os.replace(staged, args.final)
    print("Verified PDF text, font families, public scope and page count.")
