"""Version-checked Hugo entry point shared by local builds, PDF builds and CI."""
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def environment():
    env = dict(os.environ)
    local = ROOT/'.build/tools/dart-sass'
    if (local/'sass.bat').is_file():
        env['PATH'] = str(local)+os.pathsep+env.get('PATH','')
    env.setdefault('HUGO_CACHEDIR',str(ROOT/'.build/hugo-cache'))
    pins = json.loads((ROOT/'scripts/toolchain.json').read_text())
    for command, expected in [('hugo',pins['hugo']),('sass',pins['dart_sass'])]:
        executable = shutil.which(command,path=env.get('PATH'))
        if not executable: raise ValueError(f'{command} missing; see docs/hugo-toolchain.md')
        version = subprocess.check_output([executable,'version' if command=='hugo' else '--version'],env=env,text=True)
        match = re.search(r'\b(?:v)?(\d+\.\d+\.\d+)\b',version)
        if not match or match[1] != expected:
            raise ValueError(f'{command} must be {expected}; see scripts/toolchain.json')
    return env


def run(args):
    env = environment()
    if '--check' in args:
        print('Hugo and Dart Sass match scripts/toolchain.json')
        return 0
    if '--logLevel' not in args and not any(x.startswith('--logLevel=') for x in args):
        args += ['--logLevel','info']
    result = subprocess.run(['hugo',*args],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    log = result.stdout+result.stderr
    # Remote URLs can include credential query strings; do not persist or echo them.
    log = re.sub(r'([?&](?:client_id|access_token|token|key)=)[^&\s"<>]+',r'\1[REDACTED]',log,flags=re.I)
    folder=ROOT/'.build/hugo-logs';folder.mkdir(parents=True,exist_ok=True)
    name=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    (folder/(name+'.log')).write_text(log,encoding='utf-8')
    print(log,end='')
    notices=[line for line in log.splitlines() if re.search(r'deprecat',line,re.I)]
    (folder/(name+'.deprecations.json')).write_text(json.dumps(notices,ensure_ascii=False,indent=2),encoding='utf-8')
    return result.returncode


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    try: sys.exit(run(sys.argv[1:]))
    except Exception as error:
        print(str(error),file=sys.stderr)
        sys.exit(1)
