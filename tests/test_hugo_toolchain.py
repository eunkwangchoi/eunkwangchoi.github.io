"""Contracts that prevent returning to the removed template/compiler paths."""
import json
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import run_hugo
from check_about import html_ids


class Toolchain(unittest.TestCase):
    def test_active_templates_do_not_use_deprecated_calls(self):
        for folder in ('layouts','themes/write-only/layouts'):
            for file in (ROOT/folder).rglob('*.html'):
                self.assertIsNone(re.search(r'_internal/|\.Scratch\b',file.read_text(encoding='utf-8')),str(file))
        self.assertFalse((ROOT/'layouts/partials').exists())
        self.assertFalse((ROOT/'themes/write-only/layouts/index.html').exists())

    def test_wrong_toolchain_fails_before_build(self):
        with patch.object(run_hugo.shutil,'which',return_value='hugo'),patch.object(run_hugo.subprocess,'check_output',return_value='hugo v0.100.0'):
            with self.assertRaisesRegex(ValueError,'must be'): run_hugo.environment()

    def test_missing_toolchain_fails_before_build(self):
        with patch.object(run_hugo.shutil,'which',return_value=None):
            with self.assertRaisesRegex(ValueError,'missing'): run_hugo.environment()

    def test_minified_html_anchor_attributes(self):
        self.assertEqual(html_ids('<section id=writings><h2 id="press">Title</h2><p id=\'other\'>'),
                         {'writings','press','other'})


if __name__=='__main__':unittest.main()
