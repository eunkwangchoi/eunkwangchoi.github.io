# About / CV implementation status

Local implementation, 2026-10-06. No commit, push, PR, account deletion, or deployment was performed. Specification [1] was implemented first; [2] replaces its Typst proposal with Hugo print HTML, Paged.js, and Playwright.

## Implemented

- `/about/`: compact link hub, supplied portrait derivatives, featured links, social/contact links, resource downloads, light/dark and mobile styling. Per the later user instruction, the avatar is circular, CV is the only featured link, and Instagram/GitHub/Unsplash use accessible icon badges. The user confirmed GitHub `eunkwangchoi` and Unsplash `ryanchoi`. This overrides the original three-featured-links requirement.
- `/about/cv/` and `/about/cv/en/`: shared public data, grouped writings and press, linked references and series disclosures. Existing article bodies and URLs remain intact.
- `/about/profile.json`, `/about/cv.json`, `/about/ryan.vcf`: public exports. Public source excludes phone, address and identifier fields; private/draft/cancelled records do not enter the merged output.
- Data contracts, reference validation, shared CSL bibliography, two local email signature variants, migration planning and media-status tools.
- Print templates for summary/full/Art/Tec/Ref/Etc in Korean and English; reference palette, red portrait panel, interests/language sidebars and badge crops. Contact icons use SVG to avoid glyph fallback.
- Final PDF export checks required font loading, embedding, text, metadata and summary page count. Print intermediates are removed on success or failure. `profile.pdf.enabled` remains false.
- CI build and verification; separate weekly media-status workflow emits a report. These workflows have not run remotely.

## Evidence

- 261 source records pass validation, including organization/series and archive records. Public merge contains 112 entries, 61 works and 3 media records.
- Twelve tests pass: duplicate IDs, missing references, vocabulary, featured link contracts, private fields, certificate identifiers in localized details, missing public English titles, and media redirect/soft-404 decisions. Two certificate codes missed by the earlier import were removed from public source and the validator now rejects that format.
- Fresh Hugo production output was compared byte-for-byte with a baseline built from the original source using the same version/cache. Outside About, robots and sitemaps, no differences were found. Existing KO/JA History and RSS are preserved.
- Browser checks at 390px: featured touch targets, first-screen links, no horizontal overflow, light/dark hub with JavaScript disabled, and CV series disclosure.
- All 12 print drafts rendered without detected content/sidebar overflow. Summary drafts are two pages in both languages. The user-supplied Adobe web project `zfy4plf` now loads all nine required Adobe styles; the three installed Korean styles also load. Page counts were rechecked with those fonts. Art/Tec Korean drafts have no second page for the optional second-sidebar slot; the renderer records that warning.
- The print checker now examines text bounds as well as sidebars. It caught a malformed imported organization name containing Markdown URL syntax; that record was corrected to 한국문화예술위원회 / Arts Council Korea. All twelve drafts then passed the bounds check. Seven isolated Hugo fixtures passed for same-year periods, multi-day dates, semester conversion and ongoing periods. Final PDF validation also checks that font programs are embedded, not merely named.
- A normal PDF export was deliberately attempted and failed on missing font roles. It emitted no final PDF and removed `_print`.

Local evidence: `dist-local/qa/`, `dist-local/pdf-preview/report.json`, `dist-local/pdf-preview/validation.json`, and `dist-local/signature/`. Preview PNGs now use the specified Adobe web fonts and local Korean fonts. They remain layout previews, not distributable final PDFs.

## Remaining acceptance work

1. Desktop font activation was confirmed on 2026-10-07 after the owner installed the fonts: all twelve local roles load in Chromium. Print mode now uses local PostScript aliases; the supplied public Adobe web-kit URL is retained for future web previews. Twelve local PDFs were generated from the Obsidian PDF selection, with no automatic publication. Summary is two pages in each language; full is 9 KO / 12 EN pages. Every PDF passed font-family, embedded glyph/font, Unicode text, metadata, exact pagination and overflow checks; every page was rendered with Poppler and reviewed. Windows Chromium emits these local CFF fonts as Type3 fonts, so validation checks their actual FontDescriptor names, embedded CharProcs and ToUnicode streams instead of requiring only FontFile binaries. Tec currently has no mapped CV domain and its one-page files contain the introduction/sidebar only; classification remains pending. `profile.pdf.enabled` remains false because private selected PDFs must not be automatically published.
2. Full-version English localization was completed on 2026-10-07 using the supplied `Personal History EN.md` and current Korean data: 112 public entries, 61 works, 3 media records, 83 organizations and one series. Matching source wording was reused; missing/inconsistent wording was translated. See `docs/cv-translation-review.md` for source discrepancies and descriptive-name limits. Browser verification finds no untranslated Korean in the English CV content. Date formatting supports same-year periods, multi-day events and semester fields; semester-to-month mapping uses March/September and should be confirmed against the owner's academic calendar. The web-font preview now uses the specified typography; desktop-font PDF export is now verified locally.
3. Reconcile Raindrop exports against the requested 39 writings and 12 media records. Current repository evidence supplies 38 own writings and 3 media records; the third-party interview is Press. Public Raindrop access failed. `migrate_raindrop.py` creates a local review plan, not a completed migration.
4. Supply authorized book-cover assets and confirm their order. Empty cover data intentionally hides that section rather than inventing covers.
5. Review `docs/about-history-map.json`, translation/classification TODOs and the source snapshot date. Current source records are not proof that every ongoing appointment is still current. Cancelled source items were omitted during import; a complete source-line acceptance audit remains necessary.
6. Complete media preservation copies in an approved private location, confirm original titles/dates and links, and verify real mail-client signature behavior. No private archives, account deletion, external issues or notification messages were created.
7. Complete accessibility and exact typography/geometry review after fonts are available. Current mobile tests are scoped browser checks, not a complete accessibility audit.

## Rebuild

Run from the repository in PowerShell. Use a fresh destination to avoid obsolete files left by older builds.

```powershell
$env:HUGO_CACHEDIR = Join-Path (Get-Location) '.build/hugo-cache'
python -m pip install -r requirements-about.txt
npm.cmd ci --ignore-scripts
python scripts/validate_about.py
python -m unittest discover -s tests -v
hugo --environment production --destination .build/review-site
node scripts/build_citations.mjs .build/review-site/about/cv.json
hugo --environment production --destination .build/review-site
python scripts/check_about.py --public .build/review-site
python scripts/build_signature.py
$env:PLAYWRIGHT_BROWSERS_PATH = Join-Path (Get-Location) '.build/browsers'
npx.cmd playwright install chromium --only-shell
node scripts/check_about_browser.mjs .build/review-site
node scripts/check_local_fonts.mjs
node scripts/build_cv_pdf.mjs --preview --public=.build/pdf-review
```

After configuring fonts, omit `--preview` for final export. Keep the public PDF switch off until all variants pass and visual review is complete. Never deploy `.build`, `dist-local`, or print intermediates. Private security storage and independent web/PDF selections are now implemented through an external Obsidian master. See `docs/cv-private-management.md`. Normal builds never mount it; selected PDFs remain local. No private values were imported.

## Private CV update — 2026-10-07

Created an external Obsidian master with 261 records and empty security objects, preserving current public selections. A loopback-only editor provides 177 selectable CV items (including the existing draft) with independent web/PDF checkboxes. Mobile checks at 390px pass; requests without the session token receive 403. Seventeen unit tests cover public validation, security field exclusion, independent selection, dependency pruning, rollback and remaining public-copy detection. Twelve selected print previews rendered with no detected layout overflow. Adobe desktop probing after CC was opened still failed for all nine Adobe roles; three Korean roles loaded. Final PDF export remains blocked by fonts. Public source selections were not exported or deployed during this update.

## Final local PDF verification — 2026-10-07

All 12 PDFs are under ignored `dist-local/private-pdf-site/about`. Fixed duplicate original-article printing by passing detached content to Paged.js, and prevented inherited split-article justification from spreading heading/date/final-line text. Added exact PDF/Paged page-count and per-page folio checks; corrected ISBN substring false positives without allowing standalone phone patterns. Completed print kind coverage for selected books, art activities/columns/reports, research positions, literature certificates and miscellaneous essays. Eighteen regression tests pass, including detection of missing print-section mappings. Current output counts: summary 2/2, full 9/12, Art 2/2, Tec 1/1 (no classified records), Ref 4/6, Etc 4/5 (KO/EN). No private security fields, font binaries, commits, pushes or deployment were produced. Public web downloads remain disabled pending a separately generated public-only PDF set.

## Vertical-name correction — 2026-10-07

Moved the continuation-page name inside the sheet, replaced fixed word offsets with size-relative rotation, and gave the two name columns explicit classes. Added transformed-text sheet bounds and inter-column collision checks. Regenerated all twelve PDFs and verified complete EUNKWANG/CHOI text and nonintersecting PDF bounds on every continuation page. The two-page summaries remain two pages.

## Reference-edge name placement — 2026-10-07

Rechecked the supplied original English PDF: continuation-page vertical-name baselines are 30pt apart and the first column ink touches the left sheet edge. Replaced the earlier 15mm inset / 20mm separation with reference-style edge placement / 30pt separation. Blank font ascent/descent boxes intentionally overlap at this leading; checks now measure actual glyph ink bounds through Canvas TextMetrics, including left-edge alignment and ink collision. All twelve PDFs were regenerated; all 38 continuation pages pass. KO/EN second pages were rendered with Poppler and visually compared against the original.

## History site-chrome correction — 2026-10-07

Removed About-specific navbar layout and global primary-color overrides, and reused the original theme head resources including Bootstrap navigation JavaScript. The root language now follows the site while the CV/main content keeps its own language; this also preserves header font fallback metrics. About links and muted text inherit theme color variables. Removed automatic dark-body overrides that disagreed with the site theme. Browser checks compare exact header coordinates, colors, fonts and body colors against the original same-version build at 390px/1280px under light/dark preferences, for History and both CV languages (12 cases). Mobile collapse toggling passes. Outside About, robots and sitemaps, generated output remains byte-for-byte equal to the baseline.
