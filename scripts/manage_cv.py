"""Loopback-only CV selection editor. No authentication service or public endpoint."""
import argparse
import hashlib
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import secrets
import copy
import uuid
from cv_private import read, outside, export_public, save_master, safe, REFS
from cv_languages import canonical, edit_korean, set_override, sync, pending, needs_review, korean_fields
from validate_about import ROOT
import jsonschema

HTML = '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CV 공개·PDF 선택</title><style>body{font:16px/1.6 system-ui;margin:24px auto;padding:0 16px;max-width:900px;background:#f7f7f7;color:#222}header{position:sticky;top:0;background:#f7f7f7;padding:12px 0}button,input{min-height:44px}button{padding:0 16px}article{background:white;border:1px solid #ddd;border-radius:8px;padding:16px;margin:12px 0}label{display:inline-flex;align-items:center;gap:8px;margin-right:24px}input[type=checkbox]{width:22px}small{display:block;overflow-wrap:anywhere;color:#555}#search{box-sizing:border-box;width:100%;padding:8px}#status{min-height:26px}</style>
<h1>CV 공개·PDF 선택</h1><p>웹 공개와 PDF 포함을 독립적으로 선택합니다. 저장은 비공개 Obsidian 파일만 변경합니다. 공개본 내보내기는 현재 저장한 선택을 공개 저장소에 반영합니다. 게시·배포는 하지 않습니다.</p>
<p>보안 필드는 이 화면에서 읽거나 표시하지 않습니다. 기존에 공개한 글의 본문은 CV 선택과 별도로 관리합니다.</p>
<p>한글이 기준입니다. 영문 수정은 한글에 반영되지 않습니다. 기존 영문은 사용자 수정본으로 보존합니다. 자동 번역 서비스는 추후 연결하며, 번역·검토가 필요한 항목은 내보내기 전에 처리해야 합니다.</p>
<header><input id="search" aria-label="항목 검색" placeholder="항목 검색"><button id="save">선택 저장</button> <button id="export">저장된 웹 공개본 내보내기</button> <button id="add">한글 이력 추가</button><label><input id="dependencies" type="checkbox">기관·시리즈도 표시</label><p id="status" role="status"></p></header><main id="items"></main>
<dialog id="editor"><button id="close">닫기</button><h2>한글 원본·영문 수정</h2><p id="editor-status" role="status"></p><p>한글 및 공통 정보(JSON): 날짜·기관·분류는 모든 언어에서 공유합니다. ID는 변경할 수 없습니다. 보안 필드는 이 편집기에 입력하지 마세요.</p><textarea id="korean" aria-label="한글 및 공통 정보" rows="16"></textarea><button id="save-korean">한글·공통 정보 저장</button><p>영문 사용자 수정본은 자동 번역보다 우선합니다. 한글 변경 후에는 해당 영문을 검토하고 저장하세요. 체크를 해제하고 저장하면 자동 번역본을 사용합니다.</p><section id="translations"></section><button id="delete">이력 삭제</button></dialog>
<style>dialog{box-sizing:border-box;width:min(850px,95vw);max-height:90vh;overflow:auto;border:1px solid #aaa}textarea{box-sizing:border-box;width:100%;font:14px/1.5 monospace}pre{white-space:pre-wrap;overflow-wrap:anywhere}button{margin:4px 4px 4px 0}#translations>div{border-top:1px solid #ddd;padding:12px 0}#delete{color:#a00}</style>
<script>const token=__TOKEN__;let rows=[],revision='';const status=document.querySelector('#status');
new MutationObserver(()=>{document.querySelector('#editor-status').textContent=status.textContent}).observe(status,{childList:true});
async function api(action,body){const r=await fetch('/api/'+action,{method:body?'POST':'GET',headers:{'Content-Type':'application/json','X-CV-Token':token},body:body?JSON.stringify(body):undefined});const data=await r.json();if(!r.ok)throw Error(data.message);return data;}
let dirty=false,editing='';
function render(){const term=document.querySelector('#search').value.toLowerCase();const root=document.querySelector('#items');root.replaceChildren();for(const row of rows.filter(r=>(document.querySelector('#dependencies').checked||!['org','series'].includes(r.definition))&&(r.title+' '+r.id).toLowerCase().includes(term))){const a=document.createElement('article');const title=document.createElement('strong');title.textContent=row.title+(row.pending?' · 영문 번역/검토 필요':'');a.append(title);const id=document.createElement('small');id.textContent=row.id;a.append(id);if(!['org','series'].includes(row.definition)){for(const [key,text] of [['web','웹 공개'],['pdf','PDF 포함']]){const label=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.checked=row[key];input.onchange=()=>{row[key]=input.checked;dirty=true;status.textContent='저장하지 않은 변경이 있습니다.'};label.append(input,document.createTextNode(text));a.append(label)}}const edit=document.createElement('button');edit.textContent='원본·영문 편집';edit.onclick=()=>openEditor(row.id).catch(e=>status.textContent=e.message);a.append(edit);root.append(a)}}
async function load(){const d=await api('list');rows=d.rows;revision=d.revision;render()}
document.querySelector('#search').oninput=render;
document.querySelector('#dependencies').onchange=render;
document.querySelector('#save').onclick=async()=>{try{const d=await api('save',{revision,rows:rows.filter(r=>!['org','series'].includes(r.definition)).map(({id,web,pdf})=>({id,web,pdf}))});revision=d.revision;dirty=false;status.textContent='Obsidian에 선택을 저장했습니다.'}catch(e){status.textContent=e.message}};
document.querySelector('#export').onclick=async()=>{try{await api('export',{revision});status.textContent='저장된 선택을 공개 소스에 반영했습니다. 새 빌드가 필요합니다.'}catch(e){status.textContent=e.message}};
function guard(){if(dirty)throw Error('먼저 선택 저장을 눌러 주세요.');}
function display(v){return Array.isArray(v)?v.join('\\n'):v&&typeof v==='object'?JSON.stringify(v,null,2):v??''}
async function openEditor(id){guard();editing=id;const d=await api('record/'+encodeURIComponent(id));revision=d.revision;document.querySelector('#korean').value=JSON.stringify(d.data,null,2);const root=document.querySelector('#translations');root.replaceChildren();for(const f of d.fields){const box=document.createElement('div'),label=document.createElement('strong'),source=document.createElement('pre'),auto=document.createElement('pre'),toggle=document.createElement('input'),input=document.createElement('textarea'),save=document.createElement('button'),check=document.createElement('label');label.textContent=f.field+(f.review?' · 한글 변경 후 검토 필요':'');source.textContent='한글: '+display(f.source);auto.textContent='자동 번역: '+(display(f.automatic)||'대기 (서비스 미연결)');toggle.type='checkbox';toggle.checked=f.override!==null;check.append(toggle,document.createTextNode('사용자 수정본 사용'));input.value=display(f.override??f.automatic);input.setAttribute('aria-label',f.field+' 영문 사용자 수정');input.rows=3;save.textContent='영문 수정·검토 완료 저장';save.onclick=async()=>{try{const value=toggle.checked?(Array.isArray(f.source)?input.value.split('\\n').filter(v=>v.trim()):input.value):null;const result=await api('override',{revision,id:editing,field:f.field,value});revision=result.revision;await load();await openEditor(editing);status.textContent='영문을 저장했습니다. 한글 원본은 변경되지 않았습니다.'}catch(e){status.textContent=e.message}};box.append(label,source,auto,check,input,save);root.append(box)}if(!document.querySelector('#editor').open)document.querySelector('#editor').showModal()}
document.querySelector('#close').onclick=()=>document.querySelector('#editor').close();
document.querySelector('#save-korean').onclick=async()=>{try{const d=await api('edit',{revision,id:editing,data:JSON.parse(document.querySelector('#korean').value)});revision=d.revision;await load();await openEditor(editing);status.textContent='한글·공통 정보를 저장했습니다. 영문 검토 표시를 확인하세요.'}catch(e){status.textContent=e.message}};
document.querySelector('#add').onclick=async()=>{try{guard();const d=await api('create',{revision});await load();await openEditor(d.id);status.textContent='비공개 새 이력을 추가했습니다.'}catch(e){status.textContent=e.message}};
document.querySelector('#delete').onclick=async()=>{try{if(!confirm('이 항목을 웹·PDF의 모든 언어에서 삭제하시겠습니까?'))return;await api('delete',{revision,id:editing});document.querySelector('#editor').close();await load();status.textContent='모든 언어에서 이력을 삭제했습니다. 공개본에는 내보내기 후 반영됩니다.'}catch(e){status.textContent=e.message}};
load().catch(e=>status.textContent=e.message);</script></html>'''


def update_record(master, action, body):
    """Mutate a private record only; safe projections never contain security."""
    if action == 'create':
        row = {'definition': 'entry', 'source': 'data/cv/entries/history.yaml',
               'web': False, 'pdf': True, 'security': {},
               'data': {'id': 'history-'+uuid.uuid4().hex[:12], 'kind': 'activity',
                        'domain': 'art', 'title': {'ko': '새 이력'},
                        'period': {'start': str(datetime.date.today().year), 'precision': 'year'},
                        'weight': 1, 'status': 'active', 'visibility': 'public', 'links': []}}
        sync(row)
        master['records'].append(row)
        return row['data']['id']
    row = next(r for r in master['records'] if r['data']['id'] == body['id'] and not r.get('deleted'))
    if action == 'edit':
        trial = copy.deepcopy(row)
        edit_korean(trial, body['data'])
        schema = json.loads((ROOT/'schema/cv.schema.json').read_text(encoding='utf-8'))
        jsonschema.validate(trial['data'], {'$ref': '#/$defs/'+trial['definition'], '$defs': schema['$defs']})
        ids = {r['data']['id'] for r in master['records'] if not r.get('deleted')}
        for key in REFS:
            refs = trial['data'].get(key) or []
            if isinstance(refs, str): refs = [refs]
            if any(ref not in ids for ref in refs): raise ValueError('Unknown record reference')
        row.clear(); row.update(trial)
    elif action == 'override':
        set_override(row, body['field'], body['value'])
    elif action == 'delete':
        for other in master['records']:
            if other is row or other.get('deleted'): continue
            for key in REFS:
                refs = other['data'].get(key) or []
                if isinstance(refs, str): refs = [refs]
                if row['data']['id'] in refs: raise ValueError('Remove references before deleting')
        row['deleted'] = True
        row['web'] = row['pdf'] = False
    else: raise ValueError('Unknown record action')
    return row['data']['id']


def serve(path, port):
    path = outside(path)
    read(path)
    token = secrets.token_urlsafe(32)
    revision = lambda: hashlib.sha256(path.read_bytes()).hexdigest()
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args): pass
        def response(self, status, value, html=False):
            body = value.encode() if html else json.dumps(value, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'text/html; charset=utf-8' if html else 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
            self.end_headers(); self.wfile.write(body)
        def allowed(self):
            host = '127.0.0.1:'+str(self.server.server_port)
            return self.headers.get('Host') == host and self.headers.get('Origin', 'http://'+host) == 'http://'+host
        def do_GET(self):
            if not self.allowed(): return self.response(403, {'message':'접근할 수 없습니다.'})
            if self.path == '/': return self.response(200, HTML.replace('__TOKEN__', json.dumps(token)), True)
            if self.headers.get('X-CV-Token') != token:
                return self.response(403, {'message':'접근할 수 없습니다.'})
            master = read(path)
            if self.path.startswith('/api/record/'):
                from urllib.parse import unquote
                try:
                    row = next(r for r in master['records'] if r['data']['id'] == unquote(self.path[len('/api/record/'):]) and not r.get('deleted'))
                    fields = sync(row)
                    return self.response(200, {'data':safe(canonical(row)), 'revision':revision(),
                        'fields':[{'field':k, 'source':korean_fields(row)[k], 'automatic':v['automatic'],
                                   'override':v['override'], 'review':needs_review(v)} for k,v in fields.items()]})
                except Exception: return self.response(404, {'message':'항목을 찾을 수 없습니다.'})
            if self.path != '/api/list': return self.response(404, {'message':'잘못된 주소입니다.'})
            rows = []
            for row in master['records']:
                if row.get('deleted'): continue
                title = row['data'].get('name' if row['definition']=='org' else 'title', {})
                if not isinstance(title, dict): title = {}
                rows.append({'id':row['data']['id'], 'definition':row['definition'], 'title':title.get('ko') or row['data'].get('title_ko') or row['data'].get('title_en') or row['data']['id'], 'web':row['web'], 'pdf':row['pdf'], 'pending':len(pending(row))})
            self.response(200, {'rows':rows, 'revision':revision()})
        def do_POST(self):
            if not self.allowed() or self.headers.get('X-CV-Token') != token:
                return self.response(403, {'message':'접근할 수 없습니다.'})
            try:
                length = int(self.headers.get('Content-Length', 0))
                if not 0 < length <= 500000: raise ValueError()
                body = json.loads(self.rfile.read(length))
                if body['revision'] != revision(): return self.response(409, {'message':'파일이 변경되었습니다. 화면을 새로고침하세요.'})
                if self.path == '/api/export': export_public(path)
                elif self.path == '/api/save':
                    master = read(path)
                    allowed_ids = {r['data']['id'] for r in master['records'] if r['definition'] not in {'org', 'series'} and not r.get('deleted')}
                    changes = {r['id']:r for r in body['rows']}
                    if set(changes) != allowed_ids or len(changes) != len(body['rows']): raise ValueError()
                    for row in master['records']:
                        if row['data']['id'] not in changes: continue
                        for key in ('web','pdf'):
                            v = changes[row['data']['id']][key]
                            if type(v) is not bool: raise ValueError()
                            row[key] = v
                    save_master(path, master)
                elif self.path in {'/api/edit','/api/override','/api/create','/api/delete'}:
                    master = read(path)
                    record_id = update_record(master, self.path[len('/api/'):], body)
                    save_master(path, master)
                    return self.response(200, {'revision':revision(), 'id':record_id})
                else: raise ValueError()
                self.response(200, {'revision':revision()})
            except Exception:
                self.response(400, {'message':'처리하지 못했습니다. JSON 형식·참조·영문 번역/검토 상태를 확인하세요. 삭제 전에는 다른 항목의 참조를 제거해야 합니다. 공개 사본 충돌은 dist-local/qa/private-export-blockers.json을 확인하세요.'})
    server = HTTPServer(('127.0.0.1', port), Handler)
    print(f'CV manager: http://127.0.0.1:{server.server_port}/', flush=True)
    server.serve_forever()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--file', type=Path, required=True)
    p.add_argument('--port', type=int, default=13132)
    a = p.parse_args()
    serve(a.file, a.port)
