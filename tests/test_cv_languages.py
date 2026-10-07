"""One-way source ownership, override persistence, and deletion regression tests."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import cv_languages as lang
import cv_private as cv
from manage_cv import update_record


class Languages(unittest.TestCase):
    def row(self):
        return {'definition':'entry', 'source':'data/cv/entries/history.yaml',
                'web':True, 'pdf':True, 'security':{'phone':'SECRET-SENTINEL'},
                'data':{'id':'one', 'kind':'activity', 'domain':'art', 'weight':1,
                        'status':'active','visibility':'public',
                        'period':{'start':'2026','precision':'year'},
                        'title':{'ko':'한글 이력','en':'Existing English'},
                        'details':['한글 상세'], 'details_en':['Existing detail']}}

    def test_migration_preserves_existing_english(self):
        r = self.row(); before = copy.deepcopy(r['data'])
        lang.sync(r)
        self.assertEqual(lang.materialize(r), before)
        self.assertEqual(lang.pending(r), [])

    def test_english_override_never_changes_korean(self):
        r = self.row(); before = lang.canonical(r)
        lang.set_override(r, 'title', 'Manually revised')
        self.assertEqual(lang.canonical(r), before)
        self.assertEqual(lang.materialize(r)['title']['en'], 'Manually revised')

    def test_korean_edit_preserves_override_requires_review(self):
        r = self.row(); lang.sync(r)
        data = lang.canonical(r); data['title']['ko'] = '변경한 이력'
        lang.edit_korean(r, data)
        self.assertEqual(r['data']['title']['en'], 'Existing English')
        self.assertEqual(lang.pending(r), ['title'])
        with self.assertRaises(ValueError): lang.materialize(r)
        lang.set_override(r, 'title', 'Reviewed English')
        self.assertEqual(lang.pending(r), [])

    def test_automatic_results_never_override_manual(self):
        r = self.row(); master={'records':[r]}; lang.sync(r)
        data=lang.canonical(r); data['title']['ko']='번역 갱신'; lang.edit_korean(r,data)
        job = next(j for j in lang.jobs(master) if j['field']=='title')
        lang.apply_results(master, [dict(job, translation='Machine title')])
        r=master['records'][0]
        self.assertEqual(r['data']['title']['en'], 'Existing English')
        lang.set_override(r,'title',None)
        self.assertEqual(r['data']['title']['en'], 'Machine title')
        data=lang.canonical(r); data['title']['ko']='새 제목'
        lang.edit_korean(r,data)
        self.assertNotIn('en',r['data']['title'])
        self.assertIn('title',lang.pending(r))

    def test_stale_batch_is_rejected_atomically(self):
        r=self.row(); master={'records':[r]}; lang.set_override(r,'title',None); job=lang.jobs(master)[0]
        data=lang.canonical(r); data['title']['ko']='새 제목'; lang.edit_korean(r,data)
        before=copy.deepcopy(master)
        with self.assertRaises(ValueError): lang.apply_results(master,[dict(job,translation='Stale')])
        self.assertEqual(master,before)

    def test_deleted_korean_field_removes_english_and_metadata(self):
        r=self.row(); lang.sync(r); data=lang.canonical(r); del data['details']
        lang.edit_korean(r,data)
        self.assertNotIn('details_en',r['data'])
        self.assertNotIn('details',r['translations']['en'])

    def test_create_delete_and_shared_dates(self):
        master={'records':[]}; identifier=update_record(master,'create',{})
        r=master['records'][0]; lang.set_override(r,'title','New record')
        r['web']=True
        data=lang.canonical(r); data['period']['start']='2027'
        update_record(master,'edit',{'id':identifier,'data':data})
        self.assertEqual(cv.selected(master,'web')[0]['data']['period']['start'],'2027')
        update_record(master,'delete',{'id':identifier})
        self.assertEqual(cv.selected(master,'web'),[])
        self.assertEqual(cv.selected(master,'pdf'),[])
        self.assertEqual(lang.jobs(master),[])

    def test_references_block_deletion(self):
        a=self.row(); b=copy.deepcopy(a); b['data']['id']='two'; b['data']['works']=['one']
        with self.assertRaises(ValueError): update_record({'records':[a,b]},'delete',{'id':'one'})
        self.assertFalse(a.get('deleted',False))

    def test_custom_english_amount_tracks_shared_numeric_source(self):
        r=self.row(); r['data']['amount']={'value':100,'currency':'KRW','scope':'personal'}
        self.assertNotIn('amount',lang.sync(r))  # Normal numbers need no translation.
        r['data']['amount_display_en']='Special amount note'; lang.sync(r)
        data=lang.canonical(r); data['amount']['value']=200; lang.edit_korean(r,data)
        self.assertIn('amount',lang.pending(r))

    def test_reject_reverse_merge_and_private_fields(self):
        r=self.row(); before=copy.deepcopy(r)
        with self.assertRaises(ValueError): lang.edit_korean(r,r['data'])
        self.assertEqual(r,before)
        data=lang.canonical(r); data['phone']='SECRET'
        with self.assertRaises(ValueError): lang.edit_korean(r,data)
        self.assertNotIn('SECRET-SENTINEL',str(lang.jobs({'records':[r]})))


if __name__ == '__main__': unittest.main()
