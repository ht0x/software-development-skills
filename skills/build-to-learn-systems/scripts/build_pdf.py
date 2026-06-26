#!/usr/bin/env python3
"""
build_pdf.py — Engine dựng PDF cho course "Xây dựng hệ thống Chat & Voice".
Pipeline: Markdown (+ Mermaid) -> render Mermaid sang SVG -> HTML (syntax highlight)
          -> PDF bằng Chromium (playwright).

Cách dùng:
    python3 build_pdf.py <input.md> <output.pdf> ["Tiêu đề footer"]
"""
import sys, os, re, hashlib, subprocess, json, tempfile, html as htmllib
import markdown
from pygments.formatters import HtmlFormatter
from playwright.sync_api import sync_playwright

ASSETS = "/home/claude/chat_course/_assets"
os.makedirs(ASSETS, exist_ok=True)

# Trỏ mmdc sang chromium của playwright
with sync_playwright() as p:
    CHROME = p.chromium.executable_path

PUPPETEER_CFG = "/tmp/puppeteer_build.json"
with open(PUPPETEER_CFG, "w") as f:
    json.dump({"executablePath": CHROME,
               "args": ["--no-sandbox", "--disable-setuid-sandbox"]}, f)

MM_CFG = "/tmp/mm_build.json"
with open(MM_CFG, "w") as f:
    json.dump({"theme": "base", "themeVariables": {
        "fontFamily": "Inter, Helvetica, Arial, sans-serif",
        "fontSize": "15px",
        "primaryColor": "#eef3fb",
        "primaryBorderColor": "#3a6ea5",
        "primaryTextColor": "#16243a",
        "lineColor": "#5b7aa5",
        "secondaryColor": "#f4ede2",
        "tertiaryColor": "#f7f7f9"
    }, "flowchart": {"htmlLabels": True, "curve": "basis"},
       "sequence": {"useMaxWidth": True}}, f)


def render_mermaid(code: str) -> str:
    """Render 1 block mermaid -> đường dẫn file SVG (cache theo hash)."""
    h = hashlib.md5(code.encode("utf-8")).hexdigest()[:12]
    svg_path = os.path.join(ASSETS, f"mmd_{h}.svg")
    if not os.path.exists(svg_path):
        with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False) as t:
            t.write(code)
            mmd_in = t.name
        r = subprocess.run(
            ["mmdc", "-i", mmd_in, "-o", svg_path, "-c", MM_CFG,
             "-p", PUPPETEER_CFG, "-b", "transparent"],
            capture_output=True, text=True, timeout=180)
        if r.returncode != 0 or not os.path.exists(svg_path):
            sys.stderr.write("MERMAID FAIL:\n" + r.stderr + "\n")
            return f"<pre>[mermaid render error]\n{htmllib.escape(code)}</pre>"
    return svg_path


def preprocess_mermaid(md_text: str) -> str:
    """Thay mọi ```mermaid block bằng <img> SVG đã render."""
    pattern = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)

    def repl(m):
        svg = render_mermaid(m.group(1))
        if svg.startswith("<pre>"):
            return svg
        return f'\n<p class="diagram"><img src="file://{svg}" /></p>\n'

    return pattern.sub(repl, md_text)


CSS = r"""
@page {
  size: A4;
  margin: 20mm 16mm 20mm 16mm;
}
:root{
  --ink:#1c2733; --muted:#5d6b7a; --accent:#2f5d8a; --accent2:#b5651d;
  --line:#d9e0e8; --codebg:#f6f8fa; --codeink:#24292e; --soft:#eef3fb;
}
*{ box-sizing:border-box; }
body{
  font-family:"Inter","Segoe UI",Helvetica,Arial,sans-serif;
  color:var(--ink); font-size:10.6pt; line-height:1.62; margin:0;
  -webkit-font-smoothing:antialiased;
}
h1,h2,h3,h4{ font-weight:700; line-height:1.25; color:var(--ink); }
h1{
  font-size:23pt; color:var(--accent); margin:0 0 4px 0;
  padding-bottom:8px; border-bottom:3px solid var(--accent);
  page-break-before:always;
}
h1:first-of-type{ page-break-before:avoid; }
h2{
  font-size:16pt; margin:26px 0 8px; padding-left:11px;
  border-left:5px solid var(--accent2); color:#243646;
}
h3{ font-size:12.6pt; margin:18px 0 6px; color:var(--accent); }
h4{ font-size:11pt; margin:14px 0 4px; color:#2c3e50; }
p{ margin:7px 0; }
ul,ol{ margin:7px 0 7px 4px; padding-left:22px; }
li{ margin:3px 0; }
a{ color:var(--accent); text-decoration:none; }
strong{ color:#16222e; }
code{
  font-family:"JetBrains Mono","SFMono-Regular",Consolas,"Courier New",monospace;
  background:var(--soft); padding:1px 5px; border-radius:4px;
  font-size:9pt; color:#1a3a5c;
}
pre{
  background:var(--codebg); border:1px solid var(--line); border-radius:8px;
  padding:12px 14px; overflow-x:auto; line-height:1.45;
  font-size:8.7pt; page-break-inside:avoid; margin:10px 0;
}
pre code{ background:none; padding:0; color:var(--codeink); font-size:8.7pt; }
.codehilite{ background:var(--codebg); border:1px solid var(--line);
  border-radius:8px; margin:10px 0; page-break-inside:avoid; }
.codehilite pre{ border:none; margin:0; background:none; }
table{
  border-collapse:collapse; width:100%; margin:12px 0; font-size:9.2pt;
  page-break-inside:avoid;
}
th,td{ border:1px solid var(--line); padding:6px 9px; text-align:left;
  vertical-align:top; }
th{ background:var(--soft); color:#1f3a52; font-weight:700; }
tr:nth-child(even) td{ background:#fafbfc; }
blockquote{
  margin:12px 0; padding:10px 16px; border-left:4px solid var(--accent);
  background:#f3f7fc; border-radius:0 8px 8px 0; color:#2a3b4a;
}
blockquote p{ margin:4px 0; }
.diagram{ text-align:center; margin:16px 0; page-break-inside:avoid; }
.diagram img{ max-width:100%; max-height:235mm; }
hr{ border:none; border-top:1px solid var(--line); margin:22px 0; }
.cover{ page-break-after:always; padding-top:60mm; text-align:center; }
.cover .kicker{ color:var(--accent2); font-weight:700; letter-spacing:3px;
  font-size:11pt; text-transform:uppercase; }
.cover h1{ border:none; page-break-before:avoid; font-size:30pt; margin:12px 0; }
.cover .sub{ color:var(--muted); font-size:13pt; margin-top:6px; }
.cover .meta{ margin-top:40mm; color:var(--muted); font-size:10pt; line-height:1.9; }
.toc-box{ background:#f7f9fc; border:1px solid var(--line); border-radius:10px;
  padding:8px 20px; margin:14px 0; }
.toc-box ul{ list-style:none; padding-left:0; }
.toc-box > ul > li{ font-weight:600; margin-top:6px; }
.toc-box ul ul{ padding-left:18px; font-weight:400; font-size:9.4pt; }
"""

CALLOUT_CSS = r"""
.callout{ border-radius:8px; padding:10px 14px 10px 14px; margin:12px 0;
  page-break-inside:avoid; border:1px solid; font-size:9.6pt; }
.callout p:first-child{ margin-top:0; } .callout p:last-child{ margin-bottom:0; }
.note{ background:#eef5ff; border-color:#bcd4f3; }
.tip{ background:#eefaf0; border-color:#bfe6c8; }
.warn{ background:#fff6e9; border-color:#f0d9ab; }
.key{ background:#f3effc; border-color:#d6c8f0; }
.callout .lbl{ font-weight:700; display:block; margin-bottom:2px; }
.note .lbl{ color:#1d4e89; } .tip .lbl{ color:#1d7a3a; }
.warn .lbl{ color:#9a6212; } .key .lbl{ color:#6a3fb0; }
"""


def md_to_html(md_text: str) -> str:
    md_text = preprocess_mermaid(md_text)
    ext = ["fenced_code", "codehilite", "tables", "toc",
           "attr_list", "md_in_html", "sane_lists"]
    ext_cfg = {"codehilite": {"guess_lang": False, "noclasses": False},
               "toc": {"toc_depth": "2-3"}}
    return markdown.markdown(md_text, extensions=ext, extension_configs=ext_cfg)


def build(md_file: str, pdf_file: str, footer_title: str = ""):
    with open(md_file, encoding="utf-8") as f:
        md_text = f.read()
    body = md_to_html(md_text)
    pyg = HtmlFormatter(style="friendly").get_style_defs(".codehilite")
    full_html = f"""<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8">
<style>{CSS}\n{CALLOUT_CSS}\n{pyg}</style></head><body>{body}</body></html>"""

    html_path = pdf_file.replace(".pdf", ".html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    footer = f"""<div style="font-size:7.5pt; color:#8a97a5; width:100%;
      padding:0 16mm; display:flex; justify-content:space-between;
      font-family:Inter,Arial,sans-serif;">
      <span>{htmllib.escape(footer_title)}</span>
      <span>Trang <span class="pageNumber"></span> / <span class="totalPages"></span></span>
    </div>"""

    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox"])
        pg = b.new_page()
        pg.goto("file://" + os.path.abspath(html_path), wait_until="networkidle")
        pg.pdf(path=pdf_file, format="A4", print_background=True,
               display_header_footer=True,
               header_template="<div></div>", footer_template=footer,
               margin={"top": "20mm", "bottom": "18mm",
                       "left": "16mm", "right": "16mm"})
        b.close()
    print("OK ->", pdf_file)


if __name__ == "__main__":
    md_in = sys.argv[1]
    pdf_out = sys.argv[2]
    foot = sys.argv[3] if len(sys.argv) > 3 else ""
    build(md_in, pdf_out, foot)
