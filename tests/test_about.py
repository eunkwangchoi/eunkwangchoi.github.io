"""Contract tests for public data safety, integrity and media-link decisions."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import yaml
import copy

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_about import ROOT, records, validate, load
from archive_media import inspect


class DataContracts(unittest.TestCase):
    def test_public_records_have_print_section(self):
        vocab = load(ROOT/'data/cv/vocab.yaml')
        for lang in ('ko','en'):
            sections = vocab['sections']['pdf'][lang]
            allowed = {(s['domain'],kind) for s in sections for kind in s['kinds']}
            for _, definition, item in records():
                if definition in {'org','series','media'} or item.get('visibility')=='private' or item.get('status') in {'draft','cancelled'}:
                    continue
                kind = item.get('kind') or item.get('type')
                domain = kind if kind in {'education','volunteer'} else item.get('domain')
                self.assertIn((domain,kind), allowed, f"Unprinted {lang} record: {item['id']}")

    def setUp(self):
        self.root = ROOT
        self.state = copy.deepcopy(records())
        self.data = {p: load(p) for p in (ROOT / "data").rglob("*.yaml")}
        self.records_patch = patch("validate_about.records", return_value=self.state)
        self.load_patch = patch("validate_about.load", side_effect=lambda path: self.data[path])
        self.records_patch.start()
        self.load_patch.start()

    def tearDown(self):
        self.records_patch.stop()
        self.load_patch.stop()

    def mutate(self, name, change):
        path = self.root / name
        value = [item for origin, _, item in self.state if origin == path] if name.startswith("data/cv/") and name != "data/cv/vocab.yaml" else self.data[path]
        change(value)

    def test_current_public_data(self):
        self.assertGreater(validate(self.root), 100)

    def test_duplicate_id_across_archive_and_data(self):
        self.mutate("data/cv/works/external.yaml", lambda x: x[0].update(id="book-scrivener"))
        with self.assertRaisesRegex(ValueError, "Duplicate id"):
            validate(self.root)

    def test_broken_reference(self):
        self.mutate("data/cv/entries/history.yaml", lambda x: x[0].update(works=["missing-work"]))
        with self.assertRaisesRegex(ValueError, "missing or invalid"):
            validate(self.root)

    def test_unknown_vocabulary(self):
        self.mutate("data/cv/entries/history.yaml", lambda x: x[0].update(kind="unknown"))
        with self.assertRaisesRegex(ValueError, "unknown kind"):
            validate(self.root)

    def test_featured_note_required(self):
        self.mutate("data/me/links.yaml", lambda x: x[0].pop("note"))
        with self.assertRaisesRegex(ValueError, "note"):
            validate(self.root)

    def test_private_field_rejected_even_on_private_record(self):
        self.mutate("data/cv/entries/history.yaml", lambda x: x[0].update(visibility="private", certificate_id="hidden"))
        with self.assertRaisesRegex(ValueError, "private field"):
            validate(self.root)

    def test_public_profile_cannot_contain_phone(self):
        self.mutate("data/me/profile.yaml", lambda x: x.update(phone="private"))
        with self.assertRaisesRegex(ValueError, "phone"):
            validate(self.root)

    def test_certificate_identifier_in_localized_details(self):
        self.mutate("data/cv/entries/history.yaml", lambda x: x[0].update(details_en=["Certificate 25-R1-000001"]))
        with self.assertRaisesRegex(ValueError, "possible private identifier"):
            validate(self.root)

    def test_public_entry_requires_english_title(self):
        self.mutate("data/cv/entries/history.yaml", lambda x: x[0]["title"].pop("en"))
        with self.assertRaisesRegex(ValueError, "missing English title"):
            validate(self.root)


class Response:
    def __init__(self, url, title):
        self.url, self.title = url, title
        self.headers = self
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self, size): return f"<title>{self.title}</title>".encode()
    def geturl(self): return self.url
    def get_content_charset(self): return "utf-8"


class MediaDecisions(unittest.TestCase):
    def test_homepage_redirect_is_dead(self):
        with patch("urllib.request.urlopen", return_value=Response("https://example.org/", "News")):
            self.assertEqual(inspect({"url": "https://example.org/article/42"}, "News")["status"], "dead")

    def test_matching_article_redirect_is_moved(self):
        with patch("urllib.request.urlopen", return_value=Response("https://example.org/new/42", "Interview")):
            self.assertEqual(inspect({"url": "https://example.org/article/42"}, "Interview")["status"], "moved")

    def test_soft404_title_is_dead(self):
        with patch("urllib.request.urlopen", return_value=Response("https://example.org/article/42", "Page removed")):
            self.assertEqual(inspect({"url": "https://example.org/article/42"}, "Interview with Eunkwang Choi")["status"], "dead")


if __name__ == "__main__":
    unittest.main()
