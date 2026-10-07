"""Keep CV master/security data outside this public repository.

Nothing is committed, pushed or deployed by this tool. Public export is explicit.
"""
import argparse
import copy
import json
from pathlib import Path
import re
import sys
import subprocess
import os
import yaml
from validate_about import ROOT, records, validate

FORBIDDEN = {'phone', 'address', 'student_id', 'member_id', 'certificate_id',
             'military_id', 'private_overlay', 'security'}
REFS = {'works', 'media', 'about', 'org', 'publisher', 'outlet', 'venue', 'series'}


def outside(path):
    path = Path(path).resolve()
    if path == ROOT or ROOT in path.parents:
        raise ValueError('Private master must be outside the public repository')
    return path


def read(path):
    value = json.loads(outside(path).read_text(encoding='utf-8-sig'))
    if value.get('schema_version') != 1:
        raise ValueError('Unsupported private master version')
    ids = [x['data']['id'] for x in value['records']]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate private record IDs')
    for row in value['records']:
        if type(row['web']) is not bool or type(row['pdf']) is not bool:
            raise ValueError('web/pdf selections must be booleans')
        source = (ROOT / row['source']).resolve()
        if ROOT not in source.parents:
            raise ValueError('Invalid record source path')
    return value


def safe(value):
    if isinstance(value, dict):
        return {k: safe(v) for k, v in value.items() if k not in FORBIDDEN}
    if isinstance(value, list):
        return [safe(x) for x in value]
    return value


def save_master(path, master):
    """Atomic private save, with a recovery copy before replacing the master."""
    path = outside(path)
    temp = path.with_suffix('.pending.json')
    if path.exists():
        path.with_suffix('.previous.json').write_bytes(path.read_bytes())
    temp.write_text(json.dumps(master, ensure_ascii=False, indent=2, default=str)+'\n', encoding='utf-8')
    os.replace(temp, path)


def initialize(path, default):
    path = outside(path)
    if path.exists():
        raise ValueError('Private master already exists; refusing to overwrite')
    result = []
    for origin, kind, data in records():
        active = data.get('visibility') != 'private' and data.get('status') not in {'draft', 'cancelled'}
        row = {'definition': kind, 'source': origin.relative_to(ROOT).as_posix(),
               'data': data, 'web': active and default == 'current', 'pdf': active,
               'security': {}}
        if kind == 'frontmatter':
            raw = origin.read_bytes().decode('utf-8-sig')
            match = re.search(r'(?m)^\[cv\]\r?\n[\s\S]*?(?=^\+\+\+|^\[(?!cv[.\]]))', raw)
            if not match:
                raise ValueError('Unsupported archive CV block')
        result.append(row)
    value = {'schema_version': 1, 'profile_security': {}, 'records': result}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str)+'\n', encoding='utf-8')
    print(f'Initialized {len(result)} master records; no public source changed.')


def selected(master, target):
    rows = master['records']
    selected_rows = [r for r in rows if r['definition'] not in {'org', 'series'} and r[target] and not r.get('deleted')]
    # Organizations/series are emitted only when referenced by selected records.
    index = {r['data']['id']: r for r in rows}
    included = {r['data']['id'] for r in selected_rows}
    for row in selected_rows:
        for key in REFS:
            refs = row['data'].get(key) or []
            if isinstance(refs, str): refs = [refs]
            for ref in refs:
                if ref not in index:
                    raise ValueError('Unknown CV reference')
                if index[ref]['definition'] in {'org', 'series'}:
                    included.add(ref)
    result = []
    for row in rows:
        if row['data']['id'] not in included: continue
        from cv_languages import materialize
        item = safe(copy.deepcopy(materialize(row)))
        if row['definition'] not in {'org', 'series'}:
            item['visibility'] = 'public'
        for key in REFS:
            if key not in item: continue
            if isinstance(item[key], list): item[key] = [v for v in item[key] if v in included]
            elif item[key] not in included: item.pop(key)
        result.append({'definition':row['definition'], 'source':row['source'], 'data':item})
    return result


def print_data(path):
    rows = selected(read(path), 'pdf')
    result = {'entries': [], 'works': [], 'media': [], 'orgs': {}, 'series': []}
    for row in rows:
        item = row['data']
        kind = row['definition']
        if kind == 'org': result['orgs'][item['id']] = item
        elif kind == 'series': result['series'].append(item)
        elif kind == 'frontmatter':
            from validate_about import front_matter
            meta = front_matter(ROOT / row['source'])
            item['title'] = {'ko': item.get('title_ko') or meta['title'], 'en': item['title_en']}
            item['date'] = str(item.get('year') or meta['date'])
            result['works'].append(item)
        else: result[{'entry': 'entries', 'work': 'works', 'media': 'media'}[kind]].append(item)
    return result


def remaining_public_copies(master):
    needles = set()
    for row in master['records']:
        if row['definition'] in {'org', 'series'} or (row['web'] and not row.get('deleted')): continue
        item = row['data']
        needles.add(item['id'])
        title = item.get('title', {})
        if isinstance(title, dict): needles.update(v for v in title.values() if isinstance(v,str) and len(v)>=8)
        if len(item.get('title_en',''))>=8: needles.add(item['title_en'])
    # Scan both tracked files and non-ignored files destined for this repository.
    files = subprocess.check_output(['git','ls-files','-co','--exclude-standard','-z'],cwd=ROOT).decode('utf-8').split('\0')
    blocked = []
    for name in set(files):
        p = ROOT / name
        if not name or not p.is_file() or p.suffix.lower() not in {'.md','.yaml','.yml','.json','.toml','.html','.txt'}: continue
        if any(part in {'.build','dist-local','node_modules','public','resources','.obsidian','.env'} for part in p.relative_to(ROOT).parts): continue
        text = p.read_text(encoding='utf-8-sig',errors='replace')
        if any(value in text for value in needles): blocked.append(name)
    if blocked:
        report = ROOT / 'dist-local/qa/private-export-blockers.json'
        report.parent.mkdir(parents=True,exist_ok=True)
        report.write_text(json.dumps({'files':sorted(blocked)},ensure_ascii=False,indent=2),encoding='utf-8')
        raise ValueError('Hidden CV data remains in other public files; see ignored export blocker report')


def export_public(path):
    master = read(path)
    chosen = selected(master, 'web')
    by_id = {r['data']['id']: r for r in chosen}
    changes = {}
    groups = {}
    for row in master['records']:
        origin = ROOT / row['source']
        if row['definition'] == 'frontmatter':
            raw = origin.read_bytes().decode('utf-8-sig')
            header, body = raw.split('+++', 2)[1:]
            header = re.sub(r'(?m)^\[cv\]\r?\n[\s\S]*?(?=^\[(?!cv[.\]])|\Z)', '', header)
            if row['data']['id'] in by_id:
                def toml(value):
                    if isinstance(value, dict): return '{'+', '.join(json.dumps(k)+' = '+toml(v) for k,v in value.items())+'}'
                    if isinstance(value, list): return '['+', '.join(toml(v) for v in value)+']'
                    if value is None: raise ValueError('Null TOML value')
                    return json.dumps(value, ensure_ascii=False)
                block = '[cv]\r\n'+''.join(k+' = '+toml(v)+'\r\n' for k,v in by_id[row['data']['id']]['data'].items())
                header = header.rstrip('\r\n')+'\r\n\r\n'+block
            changes[origin] = ('+++'+header+'+++'+body).encode('utf-8')
        else:
            groups.setdefault(origin, [])
            if row['data']['id'] in by_id:
                groups[origin].append(by_id[row['data']['id']]['data'])
    for origin, items in groups.items():
        changes[origin] = yaml.safe_dump(items, allow_unicode=True, sort_keys=False).encode('utf-8')
    # Roll back every source if validation fails. No private security values are rendered.
    originals = {p: p.read_bytes() for p in changes}
    try:
        for p, value in changes.items(): p.write_bytes(value)
        validate()
        remaining_public_copies(master)
    except Exception:
        for p, value in originals.items(): p.write_bytes(value)
        raise
    # Never reuse a bibliography containing previously selected records.
    generated = ROOT / 'data/generated/citations.json'
    if generated.exists(): generated.unlink()
    print(f'Exported {len(chosen)} public records. Rebuild into a fresh directory before publication.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['init', 'list', 'select', 'export'])
    parser.add_argument('--file', type=Path, required=True)
    parser.add_argument('--default', choices=['current', 'private'], default='current')
    parser.add_argument('--id')
    parser.add_argument('--web', choices=['yes', 'no'])
    parser.add_argument('--pdf', choices=['yes', 'no'])
    args = parser.parse_args()
    try:
        if args.action == 'init': initialize(args.file, args.default)
        elif args.action == 'export': export_public(args.file)
        else:
            master = read(args.file)
            if args.action == 'list':
                for row in master['records']:
                    if row['definition'] not in {'org', 'series'}:
                        print(row['data']['id'], 'web='+str(row['web']), 'pdf='+str(row['pdf']))
            else:
                row = next(r for r in master['records'] if r['data']['id'] == args.id)
                for key in ('web', 'pdf'):
                    if getattr(args, key) is not None: row[key] = getattr(args, key) == 'yes'
                save_master(args.file, master)
                print('Selection saved privately; public source unchanged.')
    except Exception as error:
        print(f'CV operation failed ({type(error).__name__}); no private values logged.', file=sys.stderr)
        sys.exit(1)
