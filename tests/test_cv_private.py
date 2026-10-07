"""Privacy boundaries: selections must never render the security field store."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import cv_private as cv


class PrivateCV(unittest.TestCase):
    def rows(self):
        return {'records': [
            {'definition':'entry','source':'data/cv/entries/a.yaml','web':False,'pdf':True,
             'security':{'certificate_id':'SECRET-SENTINEL'},
             'data':{'id':'a','title':{'ko':'숨긴 항목','en':'Hidden'},'org':['o'], 'phone':'SECRET-SENTINEL'}},
            {'definition':'org','source':'data/cv/orgs.yaml','web':True,'pdf':True,
             'security':{},'data':{'id':'o','name':{'ko':'기관','en':'Org'}}},
            {'definition':'org','source':'data/cv/orgs.yaml','web':True,'pdf':True,
             'security':{},'data':{'id':'unused','name':{'en':'Not needed'}}}]}

    def test_independent_web_pdf_and_unused_dependencies(self):
        m = self.rows()
        self.assertEqual(cv.selected(m,'web'), [])
        self.assertEqual([r['data']['id'] for r in cv.selected(m,'pdf')], ['a','o'])

    def test_security_fields_never_enter_print_input(self):
        with patch.object(cv,'read',return_value=self.rows()):
            result = cv.print_data('outside')
        self.assertNotIn('SECRET-SENTINEL', json.dumps(result))
        self.assertEqual(result['entries'][0]['id'], 'a')

    def test_public_export_removes_hidden_content_and_restores_on_failure(self):
        with tempfile.TemporaryDirectory(dir=cv.ROOT/'.build') as tmp:
            root = Path(tmp)
            a=root/'data/cv/entries/a.yaml'; a.parent.mkdir(parents=True)
            a.write_text('old public source',encoding='utf-8')
            o=root/'data/cv/orgs.yaml'; o.write_text('old orgs',encoding='utf-8')
            with patch.object(cv,'ROOT',root), patch.object(cv,'read',return_value=self.rows()), patch.object(cv,'validate',side_effect=ValueError('reject')):
                with self.assertRaises(ValueError): cv.export_public('outside')
                self.assertEqual(a.read_text(), 'old public source')
            with patch.object(cv,'ROOT',root), patch.object(cv,'read',return_value=self.rows()), patch.object(cv,'validate'), patch.object(cv,'remaining_public_copies'):
                cv.export_public('outside')
                self.assertNotIn('Hidden', a.read_text())
                self.assertNotIn('SECRET', a.read_text())
                self.assertNotIn('Org', o.read_text())

    def test_private_master_cannot_live_in_public_repo(self):
        with self.assertRaises(ValueError): cv.outside(cv.ROOT/'dist-local/master.json')

    def test_hidden_copies_in_review_notes_block_export(self):
        with tempfile.TemporaryDirectory(dir=cv.ROOT/'.build') as tmp:
            root = Path(tmp)
            master = self.rows()
            master['records'][0]['data']['title']['en'] = 'Hidden CV item'
            (root/'review.md').write_text('Previously copied: Hidden CV item',encoding='utf-8')
            with patch.object(cv,'ROOT',root),patch.object(cv.subprocess,'check_output',return_value=b'review.md\0'):
                with self.assertRaises(ValueError): cv.remaining_public_copies(master)
                self.assertEqual(json.loads((root/'dist-local/qa/private-export-blockers.json').read_text())['files'],['review.md'])


if __name__ == '__main__': unittest.main()
