# PDF pipeline (read before rendering)

The bundled engine `scripts/build_pdf.py` turns a Markdown phase document (with
Mermaid blocks and callout divs) into a polished PDF.

Pipeline: **Markdown → render each Mermaid block to SVG (mermaid-cli) → Markdown to
HTML with syntax highlighting → HTML to PDF via headless Chromium (Playwright).**

## Usage

```bash
python3 scripts/build_pdf.py <input.md> <output.pdf> "Footer title text"
```

The script embeds a full CSS theme (A4, code highlighting via Pygments, styled
tables/blockquotes/callouts, page-break-before on each `# H1`, a footer with page
numbers). Mermaid SVGs are cached by content hash in an `_assets/` directory.

## Dependencies

See **`assets/BUILD.md`** for the full, step-by-step installation instructions
covering both macOS (Homebrew) and Ubuntu/Linux. In brief:

- `mermaid-cli` (`mmdc`) via npm.
- Chromium — install Playwright's bundled binary (`pip install playwright` →
  `playwright install chromium`); the engine uses this for both Mermaid SVG
  rendering and the final HTML→PDF step.
- Python libs: `markdown`, `pygments`, `playwright`, `pypdfium2`, `pypdf`.
- Fonts: Inter (body) and JetBrains Mono (code) — optional but recommended.

After installing, run the smoke test in `BUILD.md` to verify everything works
before building a real phase document.

## Quirk 1 — point the Mermaid CLI at a working Chromium

`mmdc` ships with Puppeteer, which often cannot find its own Chromium in sandboxes.
The engine solves this automatically: it locates Playwright's Chromium and writes a
Puppeteer config (`executablePath` + `--no-sandbox`) that `mmdc` is told to use. If
you set up the pipeline by hand elsewhere, replicate this — otherwise Mermaid
rendering fails with a Chrome launch error even though Playwright itself works.

## Quirk 2 — do NOT write course Markdown with shell heredocs

Writing large Markdown via `cat <<'EOF'` heredocs has been observed to silently drop
a leading byte of some multi-byte UTF-8 characters (notably the `0xE1` lead byte of
Vietnamese letters right after a capital "M": Một/Mở/Mẫu). The result is an invalid
UTF-8 file that the build step rejects.

**Always create/edit course Markdown with a file-creation/file-edit tool** (which
writes UTF-8 directly), not heredocs. If you must repair a corrupted file, the
specific fix for this trap is byte-level: a lone `0xBB`/`0xBA` continuation byte
immediately after `M` (`0x4D`) is always this corruption, so replace `M\xbb` →
`M\xe1\xbb` and `M\xba` → `M\xe1\xba`. Then verify the whole file decodes as UTF-8
before building.

## Always verify before delivering

1. Confirm the build printed no Mermaid render errors, and that the generated HTML
   contains no `mermaid render error` placeholder and one embedded diagram image per
   Mermaid block.
2. Render a few representative pages to PNG and look at them:

   ```python
   import pypdfium2 as pdfium
   pdf = pdfium.PdfDocument("out.pdf")
   for i in [0, 5, 16]:
       pdf[i].render(scale=1.7).to_pil().save(f"/tmp/p{i+1}.png")
   ```

   Check: accented characters render correctly, diagrams are crisp, code has syntax
   highlighting, tables and callouts look right, the footer shows page numbers.
3. Count pages and sanity-check the length against the ~1000+ source-line target.

## Fonts

The theme requests Inter / JetBrains Mono. If those fonts are not installed in the
render environment, Chromium falls back to default sans/mono — still readable but
less branded. For a consistent look across environments, install those fonts (or
edit the CSS font stack in `build_pdf.py`) before building.

## Reusing the engine across the whole course

The same `build_pdf.py` renders every phase — do not re-derive it per phase. Keep it
in the course repo (e.g. `docs/tools/build_pdf.py`) so any environment (including a
fresh session or a coding agent reading the repo) can reproduce the PDFs. Treat the
engine as part of the course's source of truth.
