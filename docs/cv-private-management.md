# Private CV management

The CV master is stored in the owner's private Obsidian repository, outside this
public checkout. The master contains each record's safe CV data, independent
`web` and `pdf` selections, a per-record `security` object, and a
`profile_security` object. Store certificate/member/student identifiers, private
phone/address and other security fields only in those security objects. They are
never copied into render input or returned by the management API. Existing
Obsidian KO/EN manuscripts are not rewritten.

The first initialization preserves existing public selections, including hiding
draft/cancelled items. All eligible records are initially selected for PDF.
Organization/series records are included only when referenced by chosen items.
Security fields start empty; no private values are fabricated or re-imported.

## Local selection editor

From PowerShell, set `$cvMaster` to the private `CV Private Master.json` file:

```powershell
python scripts/manage_cv.py --file $cvMaster
```

Open `http://127.0.0.1:13132/`. Select web visibility and PDF inclusion separately,
then save. Saving changes only the private file. The export button explicitly
updates public YAML and archive CV front matter; it does not commit, push or
deploy. The editor accepts only loopback requests, checks Host/Origin and a
per-session request token, serves no repository files, and does not expose the
security objects. It is not a remotely accessible service. Stop with Ctrl+C.
External edits cause a revision conflict instead of silently overwriting them.

CLI equivalents:

```powershell
python scripts/cv_private.py list --file $cvMaster
python scripts/cv_private.py select --file $cvMaster --id RECORD_ID --web no --pdf yes
python scripts/cv_private.py export --file $cvMaster
```

After export, rebuild into a **fresh** destination. Regenerate the CSL references
from that destination's new CV JSON and rebuild. Replace the old published output
as a complete build; copying over old output can retain obsolete files/PDFs.
Remove previously published PDFs that contain newly hidden items. The public
exporter validates the result and checks hidden record IDs/titles against other
tracked or non-ignored text files. If copies remain (including legacy pages or
review notes), it refuses export and rolls back source writes. See ignored
`dist-local/qa/private-export-blockers.json` for affected paths. This is a literal
text check, not proof against paraphrases, images or Git history.

Hiding an archive CV item removes its CV metadata only. It does not remove the
already-public article body, title, permalink or Git history. If the article
itself must become private, it needs a separate archive/history review. Previously
committed CV data may also remain in Git history; this tool does not rewrite it.
Any copies already downloaded cannot be recalled.

## Independently selected PDF

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH = Join-Path (Get-Location) '.build/browsers'
node scripts/build_cv_pdf.mjs --preview "--selection=$cvMaster"
# Once required desktop fonts are loaded, omit --preview for PDF files.
```

Selection builds keep output in ignored `dist-local/private-pdf-site`, including
items hidden on the website. The print-only data mount is removed after the run;
normal website builds never mount the private master. Security objects are not
printable fields. Generated private PDFs are never automatically published.
The normal no-selection build still uses only public CV records. Private print
builds remain subject to font/overflow and PDF verification.

The private store is a source snapshot. Edit CV data there after initializing;
future changes made directly to public source are not automatically merged back.
No synchronization, remote authentication, encryption or backup service is added.
Obsidian repository access and backups remain under the owner's control.

## Korean source and one-way English revisions

The private master's Korean fields own content. Shared dates, references and
classification apply to both languages. The manager now supports creating,
editing and soft-deleting records plus editing per-field English overrides.
Existing English is imported as a preserved override. Changes to Korean clear
automatic translation caches and flag overrides for review. Export/PDF selection
rejects unresolved translations in included records. English edits never modify
Korean. Deleted records are omitted in both languages; references must be removed
before deletion. Archive CV titles may override the archive article title through
`title_ko`, without rewriting article bodies or titles.

The owner chose to configure a translation provider later. No external translation
calls occur now. `cv_languages.py` exposes hash-checked job/result batches for a
future provider; manual English revision is available now. Personal History
Markdown manuscripts are not automatically watched or imported.

The ignored `.local/README.md` contains Korean operating instructions, with
`.local/Start-CVManager.ps1` and `.local/Build-CVPdf.ps1` launchers. Saves keep one
previous private master alongside the original; this is not a long-term backup.
