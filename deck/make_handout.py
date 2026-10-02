"""Writes the companion handout: per-slide text, speaker notes, placeholders and checks."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pptx import Presentation

NAVY = RGBColor(0x0B, 0x2A, 0x4A)
TEAL = RGBColor(0x0E, 0x7C, 0x7C)
GREY = RGBColor(0x5A, 0x64, 0x72)
AMBR = RGBColor(0x8C, 0x6D, 0x10)

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(10.5)
for s in doc.sections:
    s.top_margin = s.bottom_margin = Inches(0.7)
    s.left_margin = s.right_margin = Inches(0.8)


def h(txt, size=15, color=NAVY, space_before=14, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(txt)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = color
    return p


def body(txt, italic=False, color=None, size=10.5, space_after=4, bullet=False):
    p = doc.add_paragraph(style="List Bullet" if bullet else None)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(txt)
    r.italic = italic
    r.font.size = Pt(size)
    if color:
        r.font.color.rgb = color
    return p


# ---------------------------------------------------------------- cover
t = doc.add_paragraph()
t.paragraph_format.space_after = Pt(2)
r = t.add_run("Formation Damage During Drilling")
r.bold = True
r.font.size = Pt(22)
r.font.color.rgb = NAVY
t = doc.add_paragraph()
r = t.add_run("Companion handout — on-slide text, speaker notes and pre-submission checklist")
r.font.size = Pt(11.5)
r.font.color.rgb = GREY

h("What is in the deck file", size=14)
body("Formation_Damage_Drilling.pptx — 23 visible slides plus 5 hidden backup slides "
     "(B1–B5). 16:9 widescreen, Calibri throughout, every slide carries speaker notes.")
body("All figures are vector-quality PNGs (300 dpi) drawn for this deck; nothing is "
     "screenshotted from a third party, so every figure caption can say “Schematic by "
     "author.” Where you prefer a published image (e.g. the SEM on slide 10), replace the "
     "picture and put the real citation in the source line.")
body("Slides 16, 17 and 20 carry the amber ILLUSTRATIVE DATA tag, as specified.")

h("Numbers — recomputed and confirmed", size=14)
body("Every headline number in your text reproduced exactly from k = 100 md, "
     "ks = 20 md, h = 50 ft, rw = 0.354 ft, re = 745 ft, rs = 3 ft, μ = 1 cP, "
     "B = 1.2 rb/STB, p̄ = 3,500 psi, pwf = 2,500 psi:")
for line in ["S = (100/20 − 1)·ln(3/0.354) = 8.55",
             "J undamaged = 4.27 STB/d/psi → q = 4,270 STB/d (exact value 4,274)",
             "J damaged = 1.91 STB/d/psi → q = 1,910 STB/d (exact value 1,909)",
             "FE = 0.447, rate loss = −55%",
             "Δp_skin = 141.2 q B μ S / (k h) = 553 psi",
             "After acidising to S = 2: q = 3,310 STB/d → gain 1,405 STB/d",
             "1,405 × 0.5 × $30 = $21,075/day → $300,000 ÷ 21,075 = 14.2 days",
             "ln(re/rw) − 0.75 = 6.90 (slide 7 says ≈ 6.9)",
             "≈ 30% of drawdown within 3 ft (exact 31%)"]:
    body(line, bullet=True, size=10)
body("One rounding note: your slide 2 line labels are J = 4.27 and 1.91 (rounded to two "
     "decimals), which give 4,270 and 1,910 STB/d. Slide 16 uses the more precise 4,274 → "
     "1,909. The deck presents them exactly as you wrote them (4,270 / 1,910 on slides 2 "
     "and 16, 8.55 on slide 16, 8.5 in the slide 2 title and chart labels), so the deck is "
     "internally consistent — but if a supervisor recomputes, expect 4,274/1,909. "
     "If you prefer full precision, say the word and I will switch slide 2 to S = 8.55 and "
     "4,274/1,909 everywhere.", color=AMBR)

h("Placeholders to fill before submitting", size=14)
for line in ["Slide 1 — [Your Name], [Prof. Name], [University], [Month Year], "
             "image credit line at the bottom left",
             "Slide 10 — source line offers “[Or: SEM image, source, year]”",
             "Slide 23 — references 9–12 (recent papers, 2018–2025) from your literature "
             "table, plus [your.email@university]",
             "Check the four clay descriptions on slide 11 and the fluid comparison on B5 "
             "against your course notes",
             "Verify all reference details (volume, pages, editions) in your library"]:
    body(line, bullet=True, size=10)

h("How the slides map to your layout codes", size=14)
body("L1 title (slide 1) · L2 chart-led (2, 19 uses table + tree) · L3 text + figure "
     "(5, 6, 9, 10, 11, 12, 13, 18, 20) · L4 equation-centred (7, 15) · L5 table + chart "
     "(14, 16, 17, 19, B5) · L6 three columns (3, 22) · L7 five boxes (4, 8, 21) · "
     "L8 references (23). The section tracker appears on slides 5–21 only, as specified, "
     "with the correct active segment per slide.")

doc.add_page_break()

# ---------------------------------------------------------------- per slide
prs = Presentation("Formation_Damage_Drilling.pptx")
h("Slide-by-slide text and speaker notes", size=16, space_before=0)
for i, slide in enumerate(prs.slides, 1):
    vis = "backup, hidden" if i > 23 else "visible"
    label = f"Slide {i}" if i <= 23 else f"Backup B{i-23}"
    h(f"{label}  ({vis})", size=12.5, color=TEAL, space_before=12, space_after=3)
    chunks = []
    for sh in slide.shapes:
        if sh.has_text_frame:
            txt = "\n".join(p.text for p in sh.text_frame.paragraphs if p.text.strip())
            if txt.strip():
                chunks.append(txt.strip())
        if getattr(sh, "has_table", False) and sh.has_table:
            rows = ["  |  ".join(c.text.strip() for c in row.cells)
                    for row in sh.table.rows]
            chunks.append("\n".join(rows))
    body("ON SLIDE — " + "   ▪   ".join(chunks).replace("\n", " / "), size=9,
         space_after=2)
    if slide.has_notes_slide:
        nt = slide.notes_slide.notes_text_frame.text.strip()
        if nt:
            body("NOTES — " + nt, italic=True, color=GREY, size=9, space_after=8)

doc.add_page_break()
h("Editing tips (from your brief)", size=15, space_before=0)
body("PowerPoint equations: press Alt + = , type the linear text, then press Space or "
     "Enter to convert. Greek letters: type \\mu then Space. Example for slide 15: "
     "S=(k/k_s-1)ln(r_s/r_w). If the bar over p causes trouble, use p_avg on every slide "
     "instead — consistency matters more than notation.")
body("The deck currently sets the equations as formatted text boxes with true "
     "sub/superscripts, so they read correctly in PowerPoint without conversion. If your "
     "department requires equation objects, retype them with Alt + = using the strings "
     "above; the layout leaves room.")
body("Before submitting: recount words in any bullet you edit (they are ≤ 8 words by "
     "design), keep the ILLUSTRATIVE DATA tags on slides 16, 17 and 20, and give a real "
     "citation on any figure you did not draw yourself.")

doc.save("Formation_Damage_Handout.docx")
print("handout saved")
