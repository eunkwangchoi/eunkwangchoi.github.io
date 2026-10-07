"""Install the pinned official Windows Dart Sass release inside ignored .build."""
import hashlib
import io
import json
from pathlib import Path
import platform
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def setup():
    if platform.system() != 'Windows' or platform.machine().lower() not in {'amd64', 'x86_64'}:
        raise ValueError('This local installer supports Windows x64; install the pinned Sass on PATH elsewhere.')
    version = json.loads((ROOT/'scripts/toolchain.json').read_text())['dart_sass']
    target = ROOT/'.build/tools/dart-sass'
    if (target/'sass.bat').exists():
        print('Workspace Dart Sass is already installed; run scripts/run_hugo.py to verify its version.')
        return
    def fetch(url):
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'CV-Hugo-Toolchain'}),timeout=60) as response:
            return response.read()
    release = json.loads(fetch('https://api.github.com/repos/sass/dart-sass/releases/tags/'+version))
    name = f'dart-sass-{version}-windows-x64.zip'
    asset = next(a for a in release['assets'] if a['name'] == name)
    url = f'https://github.com/sass/dart-sass/releases/download/{version}/{name}'
    if asset['browser_download_url'] != url: raise ValueError('Unexpected release asset URL')
    payload = fetch(url)
    sha = 'sha256:'+hashlib.sha256(payload).hexdigest()
    if asset.get('digest') != sha: raise ValueError('Official asset digest missing or mismatched')
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        base = target.parent.resolve()
        for item in archive.infolist():
            resolved = (base/item.filename).resolve()
            if target.resolve() not in resolved.parents and resolved != target.resolve():
                raise ValueError('Unsafe archive member')
        archive.extractall(base)
    print('Installed verified Dart Sass '+version+' in .build/tools/dart-sass')


if __name__ == '__main__': setup()
