# BUILD.md — PDF pipeline setup

This file documents every dependency needed to run `docs/tools/build_pdf.py`,
the engine that turns Markdown + Mermaid phase documents into polished PDFs.

Follow the section for your environment:

- **macOS** — local machine, Homebrew.
- **Windows (PowerShell)** — local machine, Chocolatey / winget.
- **Windows (Git Bash / WSL2)** — local machine, Linux-compatible shell.
- **Ubuntu / Linux** — Claude Code sandbox + DigitalOcean / Vultr servers.

After setup, run the smoke test at the bottom to confirm everything works before
building a real phase.

---

## macOS setup (Homebrew)

### 1. Node.js + mermaid-cli (mmdc)

```bash
# Install Node if not already present
brew install node

# Install the Mermaid CLI globally
npm install -g @mermaid-js/mermaid-cli

# Confirm
mmdc --version
```

### 2. Python 3 + pip

macOS ships with Python 3. Install pip if needed:

```bash
# Ensure pip is available
python3 -m ensurepip --upgrade
```

### 3. Python libraries

```bash
pip3 install markdown pygments playwright pypdfium2 pypdf
```

### 4. Playwright's Chromium (used by both the PDF renderer and mermaid-cli)

```bash
# Install Chromium managed by Playwright
python3 -m playwright install chromium

# Confirm the binary path (you'll see something like
# /Users/you/Library/Caches/ms-playwright/chromium-xxx/chrome-mac/Chromium.app/…)
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    print('Chromium:', p.chromium.executable_path)
"
```

### 5. Fonts (Inter + JetBrains Mono)

The PDF theme uses Inter (body) and JetBrains Mono (code). Without them Chromium
falls back to system defaults — readable but less polished.

```bash
# Option A — Homebrew Cask (easiest)
brew install --cask font-inter
brew install --cask font-jetbrains-mono

# Option B — download and install manually
# Inter:         https://fonts.google.com/specimen/Inter
# JetBrains Mono: https://www.jetbrains.com/lp/mono/
# Drag .ttf/.otf files into Font Book.app
```

After installing, restart any open terminal so the font cache is refreshed.

---

## Windows setup — PowerShell (Chocolatey / winget)

> Use this if you work in PowerShell or the built-in Windows Terminal.
> Run all commands in **PowerShell** (not cmd.exe — cmd lacks the path handling
> needed for `mmdc` and `playwright`).

### 1. Node.js

```powershell
# Option A — Chocolatey
choco install nodejs -y

# Option B — winget
winget install OpenJS.NodeJS

# Confirm
node --version
npm --version
```

### 2. mermaid-cli

```powershell
npm install -g @mermaid-js/mermaid-cli
mmdc --version
```

### 3. Python 3

```powershell
# Option A — Chocolatey
choco install python -y

# Option B — winget
winget install Python.Python.3

# Option C — Microsoft Store: search "Python 3.x" and install
# Confirm
python --version
pip --version
```

### 4. Python libraries

```powershell
pip install markdown pygments playwright pypdfium2 pypdf
```

### 5. Playwright's Chromium

```powershell
python -m playwright install chromium

# Confirm the path
python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    print('Chromium:', p.chromium.executable_path)
"
```

### 6. Fonts

```powershell
# Download Inter and JetBrains Mono, then double-click each .ttf file
# and click "Install" in the Windows Font Viewer.

# Inter: https://github.com/rsms/inter/releases/latest
# JetBrains Mono: https://www.jetbrains.com/lp/mono/

# Or install via Chocolatey (if font packages are available in your feed):
# choco install font-inter font-jetbrainsmono
```

> **Path note:** `build_pdf.py` uses Python's `os.path` and `pathlib`, so it
> handles Windows paths correctly. Always invoke it as
> `python docs\tools\build_pdf.py …` (backslash or forward-slash both work in
> PowerShell).

---

## Windows setup — Git Bash / WSL2

> Use this if you already have Git for Windows (which includes Git Bash) or
> Windows Subsystem for Linux (WSL2). Both give you a Linux-compatible shell
> where the Ubuntu instructions work almost identically.

### Git Bash

Git Bash ships with a minimal Unix environment. Install Node and Python via their
Windows installers (same as PowerShell section above), then run all subsequent
commands inside Git Bash exactly as written in the Ubuntu section below.

One difference: use `python` instead of `python3` inside Git Bash on Windows:

```bash
python -m playwright install chromium
python -m pip install markdown pygments playwright pypdfium2 pypdf
```

### WSL2 (recommended for a fully Linux-equivalent environment)

```bash
# Inside your WSL2 distro (Ubuntu recommended):
# Follow the Ubuntu/Linux section below — every command is identical.
wsl --install          # if WSL2 is not yet enabled (run in PowerShell as Admin)
wsl --install -d Ubuntu
```

Then open the Ubuntu terminal and proceed with the Ubuntu section.

> **Font note for WSL2:** fonts installed on the Windows host are automatically
> available to Chromium running inside WSL2 — no separate font install needed.

---

## Ubuntu / Linux setup (apt + pip)

> This is what Claude Code's sandbox runs. If you copy-paste these commands into
> a fresh Ubuntu server or a CI container, everything will work the same way.

### 1. System packages

```bash
sudo apt-get update -y
sudo apt-get install -y \
    nodejs npm \
    python3 python3-pip \
    fontconfig \
    libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libasound2
```

> The last two lines are Chromium runtime dependencies on Ubuntu. Skip any that
> are already installed — apt will just no-op them.

### 2. mermaid-cli

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc --version
```

### 3. Python libraries

```bash
# Use --break-system-packages on Ubuntu 23.04+ (PEP 668 restriction)
pip3 install markdown pygments playwright pypdfium2 pypdf \
    --break-system-packages
```

### 4. Playwright's Chromium

```bash
python3 -m playwright install chromium --with-deps

# Confirm
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    print('Chromium:', p.chromium.executable_path)
"
```

### 5. Fonts

```bash
# Inter
mkdir -p ~/.local/share/fonts
cd /tmp
curl -L "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip" \
    -o Inter.zip
unzip -o Inter.zip "*.ttf" -d ~/.local/share/fonts/
fc-cache -fv

# JetBrains Mono
curl -L "https://download.jetbrains.com/fonts/JetBrainsMono-2.304.zip" \
    -o JBMono.zip
unzip -o JBMono.zip "fonts/ttf/*.ttf" -d /tmp/jbmono/
cp /tmp/jbmono/fonts/ttf/*.ttf ~/.local/share/fonts/
fc-cache -fv

# Verify fonts are registered
fc-list | grep -i "Inter\|JetBrains"
```

---

## Smoke test (run after setup, both platforms)

This test builds a minimal sample document and verifies every component works:
Mermaid rendering, syntax highlighting, callout divs, Vietnamese text, footer.

```bash
python3 - << 'EOF'
import subprocess, sys, tempfile, os

md = """
<div class="cover">
<div class="kicker">Test</div>
<h1>Smoke Test</h1>
<div class="sub">Pipeline verification</div>
</div>

# Heading

Text with **bold**, `inline code`, and Vietnamese: Một hệ thống tốt.

```mermaid
graph LR
    A["Client"] -->|WebSocket| B["Server"]
    B --> C[("PostgreSQL")]
```

## Code

```csharp
public async Task<string> PingAsync() => "pong";
```

<div class="callout key" markdown="1">
<span class="lbl">◆ Core concept</span>
Callout body — make sure this box renders with a coloured border.
</div>

| Col A | Col B |
|-------|-------|
| Row 1 | Data |
"""

with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                  encoding="utf-8") as f:
    f.write(md); tmp_md = f.name

pdf = tmp_md.replace(".md", ".pdf")
r = subprocess.run(
    ["python3", "docs/tools/build_pdf.py", tmp_md, pdf, "Smoke test footer"],
    capture_output=True, text=True)
if r.returncode != 0 or not os.path.exists(pdf):
    print("FAIL\n", r.stderr); sys.exit(1)

from pypdf import PdfReader
pages = len(PdfReader(pdf).pages)
print(f"✅  PDF built OK — {pages} page(s) — {pdf}")

# Render page 1 to PNG for visual check
from pypdfium2 import PdfDocument
PdfDocument(pdf)[0].render(scale=1.5).to_pil().save("/tmp/smoke_p1.png")
print("📄  Page image saved to /tmp/smoke_p1.png — open it and check:")
print("    • Mermaid diagram is rendered (not placeholder text)")
print("    • Syntax highlighting on the C# block")
print("    • Coloured callout box")
print("    • Vietnamese 'Một hệ thống tốt.' is intact (no garbled chars)")
print("    • Footer shows 'Smoke test footer  Trang 1 / N'")
EOF
```

Expected output:
```
✅  PDF built OK — 2 page(s) — /tmp/…smoke_test….pdf
📄  Page image saved to /tmp/smoke_p1.png — open it and check: …
```

If you see a Mermaid launch error, re-check that `mmdc` can find Chromium — the
engine handles this automatically, but if Playwright's Chromium moved (e.g. after
an update), re-run `python3 -m playwright install chromium`.

---

## Using the engine

```bash
python3 docs/tools/build_pdf.py \
    docs/phases/phaseN.md \
    docs/phases/phaseN.pdf \
    "Course Name · Phase N — Title"
```

Mermaid SVGs are cached in `docs/tools/_assets/` by content hash — re-renders are
fast unless the diagram source changes. Commit that directory too so CI doesn't
re-render on every run.

---

## Troubleshooting quick-reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| `mmdc` not found | npm global bin not in PATH | Add `$(npm prefix -g)/bin` to PATH (macOS/Linux) or `%APPDATA%\npm` to PATH (Windows) |
| Mermaid Chrome launch error | mmdc can't find Chromium | build_pdf.py auto-fixes this; if it still fails, re-run `playwright install chromium` |
| `UnicodeDecodeError` on build | File written via heredoc (byte corruption) | Write Markdown via a file-creation tool, not shell heredoc; see pdf-pipeline.md |
| Font fallback (no Inter/JBMono) | Fonts not installed | Run font install steps above; rebuild |
| `pip3: command not found` (Ubuntu) | Python installed without pip | `sudo apt-get install python3-pip` |
| `--break-system-packages` error | Ubuntu 23.04+ PEP 668 | Add that flag to pip3 install commands |
| PDF page count is 1 when expecting more | Phase doc has `# H1` only at top | Each `# H1` triggers a page break; that's intentional and correct |
| `python` not found (macOS/Linux) | System uses `python3` | Replace `python` with `python3` in all commands |
| `mmdc` hangs indefinitely (Windows) | Chromium sandboxing issue | `build_pdf.py` passes `--no-sandbox` automatically; if still hanging, re-install Playwright: `python -m playwright install chromium --force` |
| Permission denied on `npm install -g` (Windows) | PowerShell not run as Admin | Right-click PowerShell → "Run as Administrator", then re-run the npm command |
| `playwright` import error after install (Windows) | pip installed to wrong Python | Run `python -m pip install playwright` instead of bare `pip install playwright` to target the correct interpreter |
