"""Korean-owned CV fields and one-way English translation state.

No network requests. A future provider consumes pending jobs and returns results
through apply_results; only Korean field hashes can authorize those results.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

DICT_FIELDS = ('title', 'name', 'description', 'recent_label')
PAIRS = {'details': 'details_en', 'advisor': 'advisor_en', 'extent': 'extent_en',
         'title_ko': 'title_en', 'amount': 'amount_display_en'}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def korean_fields(row):
    data = row['data']
    result = {k: v['ko'] for k, v in data.items()
              if k in DICT_FIELDS and isinstance(v, dict) and v.get('ko')}
    result.update({k: data[k] for k in PAIRS if data.get(k) and
                   (k != 'amount' or data.get('amount_display_en') or
                    'amount' in row.get('translations', {}).get('en', {}))})
    return result


def english(data, field):
    return data.get(field, {}).get('en') if field in DICT_FIELDS else data.get(PAIRS[field])


def write_english(data, field, value):
    if field in DICT_FIELDS:
        if isinstance(data.get(field), dict): data[field].pop('en', None)
        if value is not None: data.setdefault(field, {})['en'] = copy.deepcopy(value)
    else:
        data.pop(PAIRS[field], None)
        if value is not None: data[PAIRS[field]] = copy.deepcopy(value)


def sync(row):
    """Keep translations under the same record ID; never write Korean fields."""
    fields = row.setdefault('translations', {}).setdefault('en', {})
    source = korean_fields(row)
    for field in set(fields) - set(source):
        del fields[field]
        write_english(row['data'], field, None)
    for field, value in source.items():
        sha = digest(value)
        if field not in fields:
            old = english(row['data'], field)
            fields[field] = {'source_hash': sha, 'automatic': None,
                             'override': copy.deepcopy(old), 'override_hash': sha if old else None}
        state = fields[field]
        if state['source_hash'] != sha:
            state['source_hash'] = sha
            state['automatic'] = None
        effective = state['override'] if state['override'] is not None else state['automatic']
        write_english(row['data'], field, effective)
    return fields


def needs_review(state):
    return state['override'] is not None and state.get('override_hash') != state['source_hash']


def pending(row):
    if row.get('deleted'): return []
    return [field for field, state in sync(row).items()
            if (state['override'] is None and state['automatic'] is None) or needs_review(state)]


def materialize(row):
    row = copy.deepcopy(row)
    if 'translations' in row:
        if pending(row):
            raise ValueError('English translation or override review required before export')
    return row['data']


def canonical(row):
    data = copy.deepcopy(row['data'])
    for field in DICT_FIELDS:
        if isinstance(data.get(field), dict): data[field].pop('en', None)
    for target in PAIRS.values(): data.pop(target, None)
    return data


def edit_korean(row, data):
    """Reject English input in the Korean editor rather than merging it back."""
    from cv_private import safe
    if data != safe(data): raise ValueError('Security fields must stay in the private security store')
    if data.get('id') != row['data']['id']: raise ValueError('Record ID cannot change')
    if any(k in data for k in PAIRS.values()): raise ValueError('Use the English override editor')
    if any(isinstance(data.get(k), dict) and 'en' in data[k] for k in DICT_FIELDS):
        raise ValueError('Use the English override editor')
    sync(row)  # Capture existing English before replacing canonical input.
    row['data'] = copy.deepcopy(data)
    sync(row)


def set_override(row, field, value):
    states = sync(row)
    if field not in states: raise ValueError('Unknown Korean field')
    source = korean_fields(row)[field]
    valid = (isinstance(value, list) and all(isinstance(v, str) and v.strip() for v in value)
             and len(value) == len(source)) if isinstance(source, list) else isinstance(value, str) and bool(value.strip())
    if value is not None and not valid: raise ValueError('Translation type/length must match Korean source')
    states[field]['override'] = copy.deepcopy(value)
    states[field]['override_hash'] = states[field]['source_hash'] if value is not None else None
    sync(row)


def jobs(master):
    result = []
    for row in master['records']:
        if row.get('deleted'): continue
        for field, state in sync(row).items():
            if state['automatic'] is None and (state['override'] is None or needs_review(state)):
                result.append({'id': row['data']['id'], 'field': field, 'language': 'en',
                               'source_hash': state['source_hash'], 'source': korean_fields(row)[field]})
    return result


def apply_results(master, results):
    """Validate an entire batch before changing anything; preserve overrides."""
    trial = copy.deepcopy(master)
    index = {row['data']['id']: row for row in trial['records'] if not row.get('deleted')}
    seen = set()
    for result in results:
        if result.get('language') != 'en': raise ValueError('Only English is currently supported')
        key = (result['id'], result['field'])
        if key in seen: raise ValueError('Duplicate result')
        seen.add(key)
        row = index[result['id']]
        state = sync(row)[result['field']]
        if result['source_hash'] != state['source_hash']: raise ValueError('Stale translation result')
        source, value = korean_fields(row)[result['field']], result['translation']
        valid = (isinstance(value, list) and len(value) == len(source)
                 and all(isinstance(v, str) and v.strip() for v in value)) if isinstance(source, list) else isinstance(value, str) and bool(value.strip())
        if not valid: raise ValueError('Translation type/length must match Korean source')
        state['automatic'] = copy.deepcopy(value)
        sync(row)
    master.clear()
    master.update(trial)


def migrate(master):
    from validate_about import ROOT, front_matter
    master['language_policy'] = {'source': 'ko', 'targets': ['en'], 'provider': None}
    for row in master['records']:
        if row['definition'] == 'frontmatter' and 'title_ko' not in row['data']:
            row['data']['title_ko'] = front_matter(ROOT / row['source'])['title']
        sync(row)


if __name__ == '__main__':
    from cv_private import read, outside, save_master
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['migrate', 'pending', 'apply'])
    p.add_argument('--file', required=True, type=Path)
    p.add_argument('--exchange', type=Path)
    a = p.parse_args()
    try:
        master = read(a.file)
        if a.action == 'migrate':
            migrate(master)
            save_master(a.file, master)
        elif a.action == 'pending':
            outside(a.exchange).write_text(json.dumps(jobs(master), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        else:
            apply_results(master, json.loads(outside(a.exchange).read_text(encoding='utf-8-sig')))
            save_master(a.file, master)
        print('Private language operation completed; public source unchanged.')
    except Exception as error:
        import sys
        print(f'Language operation failed ({type(error).__name__}); private values not logged.', file=sys.stderr)
        sys.exit(1)
