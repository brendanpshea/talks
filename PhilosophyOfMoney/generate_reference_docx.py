"""
generate_reference_docx.py
Creates a reference.docx for pandoc with:
  - Garamond 10pt for body / list styles
  - Deep navy headings (#2c4a7c), sized 18 / 13 / 11 pt
Run once; pandoc picks it up via --reference-doc=reference.docx
"""

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import copy, os

HEADING_COLOR = RGBColor(0x2C, 0x4A, 0x7C)   # deep navy blue
BODY_FONT     = "Garamond"

def set_run_font(run, name, size_pt, bold=False, italic=False, color=None):
    run.font.name  = name
    run.font.size  = Pt(size_pt)
    run.font.bold  = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color

def style_paragraph_font(style, name, size_pt, bold=False, italic=False, color=None):
    f = style.font
    f.name  = name
    f.size  = Pt(size_pt)
    f.bold  = bold
    f.italic = italic
    if color:
        f.color.rgb = color

def main():
    doc = Document()

    # ── Normal / body text ──────────────────────────────────────────
    normal = doc.styles["Normal"]
    style_paragraph_font(normal, BODY_FONT, 10)
    normal.paragraph_format.space_after  = Pt(4)
    normal.paragraph_format.line_spacing = Pt(15)

    # ── Heading 1 ───────────────────────────────────────────────────
    h1 = doc.styles["Heading 1"]
    style_paragraph_font(h1, BODY_FONT, 18, bold=True, color=HEADING_COLOR)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after  = Pt(4)
    h1.paragraph_format.keep_with_next = True

    # ── Heading 2 ───────────────────────────────────────────────────
    h2 = doc.styles["Heading 2"]
    style_paragraph_font(h2, BODY_FONT, 13, bold=True, color=HEADING_COLOR)
    h2.paragraph_format.space_before = Pt(10)
    h2.paragraph_format.space_after  = Pt(3)
    h2.paragraph_format.keep_with_next = True

    # ── Heading 3 ───────────────────────────────────────────────────
    h3 = doc.styles["Heading 3"]
    style_paragraph_font(h3, BODY_FONT, 11, bold=True, italic=True, color=HEADING_COLOR)
    h3.paragraph_format.space_before = Pt(8)
    h3.paragraph_format.space_after  = Pt(2)
    h3.paragraph_format.keep_with_next = True

    # ── List Paragraph ──────────────────────────────────────────────
    try:
        lp = doc.styles["List Paragraph"]
    except KeyError:
        lp = doc.styles.add_style("List Paragraph", 1)  # 1 = WD_STYLE_TYPE.PARAGRAPH
    style_paragraph_font(lp, BODY_FONT, 10)
    lp.paragraph_format.left_indent  = Pt(18)
    lp.paragraph_format.space_after  = Pt(3)

    # ── Compact (Body Text) style ───────────────────────────────────
    try:
        bt = doc.styles["Body Text"]
        style_paragraph_font(bt, BODY_FONT, 10)
    except KeyError:
        pass

    out_path = os.path.join(os.path.dirname(__file__), "reference.docx")
    doc.save(out_path)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
