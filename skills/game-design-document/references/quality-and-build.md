# Quality and build

Verification checks for Phase 6, and the PDF recipe for Phase 7.

---

## Part 1 — Verification

Run all four. Each one has caught a real defect.

### 1.1 Cross-reference every identifier

The most common defect in a document of this kind is a citation pointing at the wrong rule — `F-05.R9` cited as "the invalid-action rule" when `R9` is something else. It reads fine and is completely wrong.

```python
import re, pathlib
d = pathlib.Path("<gdd path>")
defined, refs = set(), {}
for f in d.glob("*.md"):
    t = f.read_text()
    defined |= {m.group(1) for m in re.finditer(r'\|\s*\*\*(F-\d\d\.(?:R|AC)\d+)\*\*\s*\|', t)}
    for m in re.finditer(r'`(F-\d\d\.(?:R|AC)\d+)`', t):
        refs.setdefault(m.group(1), []).append(f.name)
print("defined:", len(defined))
print("dangling:", sorted(set(refs) - defined) or "none")
for r in sorted(refs):
    print(r, "<-", sorted(set(refs[r])))
```

A clean run is necessary but not sufficient. **Then read each reference against its definition** — the script proves the ID exists, not that it means what the citing sentence claims. Do the same for `[OPEN Qn]` markers against the open-questions table.

### 1.2 Render every diagram

```bash
npm install --silent @mermaid-js/mermaid-cli
echo '{"executablePath":"<chromium path>","args":["--no-sandbox","--disable-dev-shm-usage"]}' > pptr.json
# extract each ```mermaid block to its own .mmd, then:
for f in diagrams/*.mmd; do
  ./node_modules/.bin/mmdc -p pptr.json -b white -i "$f" -o "${f%.mmd}.svg" || echo "FAIL $f"
done
```

Then check the aspect ratio of each result. **Anything wider than about 2.6 : 1 will be unreadable at page width** — go back and restructure the diagram, usually by changing `LR` to `TD`.

```python
import re, pathlib
for f in sorted(pathlib.Path("diagrams").glob("*.svg")):
    m = re.search(r'viewBox="([\d.\- ]+)"', f.read_text()[:800])
    _, _, w, h = [float(x) for x in m.group(1).split()]
    print(f"{f.name:34} {w:6.0f} x {h:6.0f}  {w/h:5.2f}", "<-- TOO WIDE" if w/h > 2.6 else "")
```

Open two or three of the rendered diagrams and look at them. Overlapping edge labels and tangled crossings pass every automated check and fail a reader.

### 1.3 Scan for technical leaks

```bash
grep -rniE '\b(class |interface |namespace|schema|api|endpoint|serializ|singleton|database|<engine names>|<language names>|<library names>)\b' *.md
```

Every hit is one of three things:

- The name of a tracker item, a reference project or a tool the user named — **fine**.
- A necessary description of a player-facing behaviour — **fine**, if the mechanism is still absent.
- A leak — **remove it.**

Also grep for file paths and directory separators. A GDD should contain none except links between its own files.

### 1.4 Check stated counts

If the document says "82 criteria", "10 features" or "221 rules", count them and fix the statement. These numbers appear in several places — the README, the scope file, the acceptance index, the PDF cover — and drift apart the moment anything is added.

---

## Part 2 — Building the PDF

Markdown → HTML → PDF via headless Chromium. Produces selectable text, so every ID stays searchable.

### 2.1 Pipeline

1. **Extract and render every Mermaid block to SVG** (§1.2). Keep a stable name per block: `<file-stem>__<index>.svg`.
2. **Build one HTML document:**
   - Replace each Mermaid block with `<figure class="diagram"><img src="diagrams/<name>.svg"></figure>`.
   - Strip each file's own `#` heading — the chapter header supplies it.
   - Rewrite cross-document links (`[x](07-soil.md)`) to internal anchors (`#ch-07-soil`), so the PDF's cross-references are clickable.
   - Convert with a Markdown library with `tables`, `fenced_code` and `sane_lists` enabled.
   - Wrap each file in `<section class="chapter" id="ch-…">` with a header carrying the section number, title and source file name.
   - Prepend a cover and a contents page.
3. **Print to PDF** with Chromium via Puppeteer: A4, `printBackground: true`, margins ~17mm, a footer template with the document title and `pageNumber / totalPages`.

### 2.2 CSS that matters

```css
@page { size: A4; margin: 17mm 16mm 18mm 16mm; }
body { font-size: 10pt; line-height: 1.5; }

.chapter { break-before: page; }
h2, h3 { break-after: avoid; }
tr { break-inside: avoid; }
figure.diagram { break-inside: avoid; text-align: center; }
figure.diagram img { max-width: 100%; max-height: 165mm; }
pre { break-inside: avoid; overflow: hidden; font-size: 7.4pt; }

/* ID cells must never break mid-identifier */
td > strong:only-child { white-space: nowrap; }
```

The last rule is the one that is always missed. Without it `F-01.R10` wraps as `F-` / `01.R10` and the table becomes unreadable.

### 2.3 Verify the PDF

```python
from pypdf import PdfReader
r = PdfReader("<output>.pdf")
print("pages:", len(r.pages))
t = "".join(p.extract_text() or "" for p in r.pages)
for s in ["<a rule ID>", "<a section title>", "Contents", "Glossary"]:
    print(s, ":", s in t)
```

Then render a handful of pages to images and **look at them** — the cover, the contents, a table-heavy page, a diagram page. Automated checks do not catch a contents page that spills one entry onto a second sheet, or a diagram shrunk to nothing.

Ligature note: text extraction turns "fi" into a single glyph, so a search for `field` can fail on a page that plainly contains it. Search for a substring that avoids ligatures before concluding something is missing.

---

## Part 3 — Common failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| A diagram is a thin illegible strip | `flowchart LR` with many nodes | Change to `TD` |
| `F-01.R10` wraps mid-ID in a table | Missing `white-space: nowrap` on ID cells | Add the rule in §2.2 |
| A cited rule means something else | Citation written from memory | §1.1, then read each pair |
| The contents page spills to a second page | Line height too generous | Tighten to ~1.24 and reduce the subtitle size |
| Counts disagree between files | Content added without updating the totals | §1.4 |
| A feature file has no edge cases | The feature was not thought through | Go back to Phase 3 for that feature |
| Everything is "Must" | Priority not actually applied | Re-triage: if it cannot slip, ask what would happen if it did |
