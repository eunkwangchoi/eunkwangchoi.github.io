# Hugo build toolchain

The project uses Hugo **0.167.0** and Dart Sass **1.101.0**, pinned in
`scripts/toolchain.json`. The GitHub Pages workflow reads these same values.
The minimum Hugo version is also declared in `hugo.toml` and the active theme.

## Windows local setup

From the repository root:

```powershell
python scripts/setup_sass.py
python scripts/run_hugo.py --check
python scripts/run_hugo.py --destination .build/review-site --environment development
```

The installer downloads the official Windows x64 release into ignored
`.build/tools/dart-sass`, verifies the GitHub release asset SHA-256 before extraction,
and does not change the system PATH. The wrapper adds this directory to the child
build environment. Other systems should install the pinned Dart Sass on PATH.

Use `npm run build -- --destination ...` or `python scripts/run_hugo.py ...`
for checked builds. A wrong/missing Hugo or Sass version fails before building.
The PDF builder also calls this wrapper. Existing local PDF commands remain valid.

For Hugo's interactive server, keep a terminal-local PATH and run the version check:

```powershell
$env:PATH = (Join-Path (Get-Location) '.build/tools/dart-sass') + ';' + $env:PATH
python scripts/run_hugo.py --check
hugo server --bind 127.0.0.1 --port 13131
```

Stop an existing listener on that port before starting another preview server.

## Diagnostics

The wrapper runs INFO logging, redacts common credential URL parameters and saves
each invocation under ignored `.build/hugo-logs/`, with a separate list of
deprecation messages. CI uploads these diagnostics even when a later step fails.
Logs contain timestamps to distinguish a cached build from a fresh compiler run.
Do not infer absence of source deprecations from a cached build's empty log.

The Sass entry point explicitly selects Dart Sass. Application style modules use
`@use`. `_bootstrap.scss` is a documented legacy integration boundary because the
pinned Bootstrap 5.3.0-alpha1 source still depends on global Sass imports/functions.
Those third-party deprecation warnings remain visible. They are not suppressed,
and migration to a future Bootstrap source is a separate change with visual review.
The integration boundary's own imports also remain until that coordinated change.

## Vendor maintenance

The repository currently tracks theme files directly; `.gitmodules` also contains
legacy declarations. Do not run an automatic theme/submodule update during a normal
build. Preserve existing local theme/content changes before changing this policy.

Local compatibility changes to vendored modules are reproducible with
`patches/hugo-vendor-modernization.patch`: remove obsolete `hugoVersion.extended`
settings and move the icons partial to `_partials`. After re-vendoring from the
pinned sources, run `git apply --check patches/hugo-vendor-modernization.patch`,
then apply the patch only if the check passes. Version changes need a reviewed new
patch, not a forced application. Bootstrap library versions were not upgraded here.

The theme's Netlify configuration is a standalone legacy example, not the active
deployment. Its version declarations are aligned, but no Netlify build was run.
The Coming Soon theme is inactive; its standalone local build is tested separately.

## Regression checks

```powershell
python -m unittest discover -s tests
python scripts/check_about.py --public .build/review-site
```

`scripts/check_hugo_migration.mjs` compares visible geometry, colors, typography and
text in 22 route/viewport cases against `.build/modernization/baseline`.
`check_history_header.mjs` accepts `--baseline=... --current=...` for focused menu
comparison. These require the existing local Playwright browser runtime.

Compiler migration can change inline CSS bytes on every HTML page. Compare markup
outside `<style>` separately, then use computed styles/geometry and visual checks.
Template-path migration alone should preserve the generated output.
