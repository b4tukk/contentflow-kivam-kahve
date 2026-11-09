# -*- coding: utf-8 -*-
import sys, re, pathlib
REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "tools"))
from content_source import *

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from pptx import Presentation
from pptx.util import Inches, Pt as PPt
from pptx.dml.color import RGBColor as PRGB
from pptx.enum.text import PP_ALIGN

O = str(REPO / "deliverables"); S = f"{O}/icerik_seti"
rgb = lambda h: RGBColor(int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))
prgb = lambda h: PRGB(int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16))
ESP, CREMA, COP, SAGE, CREAM = "#3B2A20", "#E8D5B7", "#C8693A", "#7A8B6F", "#FAF6EF"

def shade(cell, hexcol):
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hexcol[1:]); tcPr.append(sh)

def newdoc(size=10, margin=1.8):
    d = Document()
    for s in d.sections:
        s.top_margin = s.bottom_margin = Cm(margin); s.left_margin = s.right_margin = Cm(2)
    st = d.styles["Normal"]; st.font.size = Pt(size); st.font.name = "Calibri"
    for n, sz in (("Heading 1", 20), ("Heading 2", 13)):
        h = d.styles[n]; h.font.name = "Georgia"; h.font.size = Pt(sz); h.font.color.rgb = rgb(ESP if n == "Heading 1" else COP)
    return d

def table(d, head, rows, widths=None, size=9):
    t = d.add_table(rows=1, cols=len(head)); t.style = "Table Grid"
    for i, h in enumerate(head):
        c = t.rows[0].cells[i]; c.text = ""; r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(size); r.font.color.rgb = rgb(CREAM); shade(c, ESP)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""; r = cells[i].paragraphs[0].add_run(str(v)); r.font.size = Pt(size)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths): row.cells[i].width = Cm(w)
    return t

def para(d, text, bold_first=None, after=3):
    p = d.add_paragraph(); p.paragraph_format.space_after = Pt(after)
    for part in re.split(r"(\*\*.+?\*\*)", text):
        if part.startswith("**"): p.add_run(part[2:-2]).bold = True
        else: p.add_run(part)
    return p

def bullet(d, text):
    p = d.add_paragraph(style="List Bullet"); p.paragraph_format.space_after = Pt(0); p.add_run(text)

# =============== 1) MARKA STRATEJİSİ DOKÜMANI (1-2 sayfa) ===============
d = newdoc(9.5, 1.5)
d.add_heading(f"{BRAND} — Marka Stratejisi", 1)
para(d, f"**Sektör:** Kahve / evde demleme eğitimi · **Slogan:** {TAGLINE} · **Değerler:** {', '.join(VALUES)}  (Kurgusal marka)")
d.add_heading("1. Marka ve rakip analizi", 2)
table(d, ["Rakip", "Konumlandırma (genel)", "Fırsat boşluğu"], COMPETITORS, [3.6, 6.2, 6.8], 8.5)
para(d, COMP_NOTE).runs[0].italic = True
d.add_heading("2. Marka kimliği", 2)
t = d.add_table(rows=1, cols=5)
for i, (n, h, u) in enumerate(PALETTE):
    c = t.rows[0].cells[i]; shade(c, h); c.text = ""
    r = c.paragraphs[0].add_run(f"{n}\n{h}"); r.font.size = Pt(8.5); r.bold = True
    r.font.color.rgb = rgb(CREAM if n in ("Espresso", "Bakır", "Adaçayı") else ESP)
para(d, "Görsel dil: düz (flat) ve sade çizimler, bol boşluk, yalnızca bu 5 renk. Yazı tipleri: başlıkta Georgia (serif), metinde Segoe UI/Calibri.", after=2)
d.add_heading("3. Neden – Kime – Ne – Nasıl", 2)
for k, v in (("Neden", WHY), ("Kime", WHO), ("Ne", WHAT), ("Nasıl", HOW)): para(d, f"**{k}:** {v}", after=1)
d.add_heading("4. Marka sesi rehberi (tek sayfa özeti)", 2)
table(d, ["Yap", "Yapma"], list(zip(TONE_DO, TONE_DONT)), [8.3, 8.3], 8.5)
para(d, f"**Tercih edilen sözcükler:** {', '.join(VOCAB)}.  **Kaçınılan:** {', '.join(AVOID)}.", after=2)
para(d, f"**Örnek cümle:** \"Bu hafta bir fincanı ölçerek demle, sonra bize tadını anlat.\"", after=2)
d.add_heading("5. İçerik sütunları", 2)
table(d, ["Sütun", "İçerik", "Hedef kitleyle bağı"], PILLARS, [3.6, 6.4, 6.6], 8.5)
d.save(f"{O}/1_Marka_Stratejisi_Dokumani.docx")

# =============== 2) İÇERİK TAKVİMİ (Excel) ===============
wb = openpyxl.Workbook(); ws = wb.active; ws.title = "7 Günlük Takvim"
ws.append(CAL_HEAD)
for r in CAL: ws.append(r)
thin = Side(style="thin", color="C9B79C")
for c in ws[1]:
    c.font = Font(bold=True, color="FAF6EF"); c.fill = PatternFill("solid", fgColor="3B2A20"); c.alignment = Alignment(wrap_text=True, vertical="center")
for row in ws.iter_rows(min_row=2):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = Border(top=thin, bottom=thin, left=thin, right=thin)
    row[3].fill = PatternFill("solid", fgColor="E8D5B7")
for col, w in zip("ABCDEFGHIJKL", (11, 11, 7, 16, 18, 16, 28, 42, 20, 20, 24, 9)): ws.column_dimensions[col].width = w
ws.freeze_panes = "A2"; ws.row_dimensions[1].height = 30
ws2 = wb.create_sheet("İçerik Sütunları"); ws2.append(["Sütun", "İçerik", "Hedef kitleyle bağı"])
for p in PILLARS: ws2.append(list(p))
for c in ws2[1]: c.font = Font(bold=True, color="FAF6EF"); c.fill = PatternFill("solid", fgColor="3B2A20")
for col, w in zip("ABC", (24, 60, 50)): ws2.column_dimensions[col].width = w
wb.save(f"{O}/2_Icerik_Takvimi.xlsx")

# =============== 3) ÖRNEK İÇERİK SETİ (metinler) ===============
d = newdoc(11)
d.add_heading(BLOG_TITLE, 1)
para(d, f"Meta açıklama: {BLOG_META}").runs[0].italic = True
para(d, f"Anahtar kelimeler: {BLOG_KEYWORDS}").runs[0].italic = True
for kind, txt in BLOG:
    if kind == "h": d.add_heading(txt, 2)
    else: para(d, txt, after=6)
d.save(f"{S}/blog_yazisi.docx")

d = newdoc(11)
d.add_heading("Sosyal Medya Gönderileri (RTF formülüyle)", 1)
for i, p in enumerate(POSTS, 1):
    d.add_heading(f"Gönderi {i} — {p['kanal']} · {p['sutun']}", 2)
    para(d, "**Kullanılan RTF istemi:** " + p["rtf"]).runs[0].font.size = Pt(9.5)
    for line in p["metin"].split("\n"): para(d, line, after=0)
    if p["gorsel"]: para(d, f"Görsel: {p['gorsel']}", after=8).runs[0].italic = True
d.save(f"{S}/sosyal_medya_gonderileri.docx")

# =============== 4) KONTROL + AI RAPORU ===============
d = newdoc(9.5, 1.6)
d.add_heading("İçerik Kontrol Listesi (Telif / Halüsinasyon / Marka Sesi)", 1)
table(d, CHK_HEAD, CHK, [2.4, 3.4, 3.8, 4.2, 4.0], 8)
d.add_heading("AI Kullanım Raporu", 1)
table(d, AI_HEAD, AI, [3.6, 3.2, 4.6, 6.4], 8.5)
d.add_heading("Prompt Kütüphanesi", 1)
for t_, p_ in PROMPTS:
    para(d, f"**{t_}:** {p_}", after=3)
d.save(f"{O}/4_Kontrol_ve_AI_Kullanim_Raporu.docx")

# =============== 5) TEK SUNUM (Canva'ya aktarılabilir) ===============
prs = Presentation(); prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
def slide(title, dark=False):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.background.fill; bg.solid(); bg.fore_color.rgb = prgb(ESP if dark else CREAM)
    tb = s.shapes.add_textbox(Inches(.6), Inches(.35), Inches(12), Inches(.9)).text_frame
    tb.text = title or ' '; r = tb.paragraphs[0].runs[0]; r.font.size = PPt(30); r.font.bold = True; r.font.name = "Georgia"; r.font.color.rgb = prgb(CREMA if dark else ESP)
    if not title: return s
    bar = s.shapes.add_shape(1, Inches(.6), Inches(1.2), Inches(1.1), Inches(.07)); bar.fill.solid(); bar.fill.fore_color.rgb = prgb(COP); bar.line.fill.background()
    return s
def text(s, x, y, w, h, lines, size=15, color=ESP, bullets=True):
    tf = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame; tf.word_wrap = True
    for i, l in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = ("• " if bullets else "") + l; p.space_after = PPt(6)
        for r in p.runs: r.font.size = PPt(size); r.font.color.rgb = prgb(color); r.font.name = "Calibri"
def ptable(s, head, rows, x, y, w, size=10, colw=None):
    shp = s.shapes.add_table(len(rows) + 1, len(head), Inches(x), Inches(y), Inches(w), Inches(.4 * (len(rows) + 1)))
    t = shp.table
    for i, h in enumerate(head):
        c = t.cell(0, i); c.text = h; c.fill.solid(); c.fill.fore_color.rgb = prgb(ESP)
        for r in c.text_frame.paragraphs[0].runs: r.font.size = PPt(size); r.font.bold = True; r.font.color.rgb = prgb(CREAM)
    for ri, row in enumerate(rows, 1):
        for ci, v in enumerate(row):
            c = t.cell(ri, ci); c.text = str(v); c.fill.solid(); c.fill.fore_color.rgb = prgb(CREAM if ri % 2 else "#F1E6D3")
            for r in c.text_frame.paragraphs[0].runs: r.font.size = PPt(size); r.font.color.rgb = prgb(ESP)
    if colw:
        for i, cw in enumerate(colw): t.columns[i].width = Inches(cw)

s = slide("", dark=True)
text(s, .8, 2.3, 11.5, 1.5, [BRAND.upper()], 60, CREMA, False)
text(s, .8, 3.6, 11.5, 1, ["ContentFlow — Yapay Zeka Destekli Marka İçerik Üretim Sistemi"], 26, CREAM, False)
text(s, .8, 4.4, 11.5, 1, [f"{TAGLINE}  ·  Yapay Zeka ile İçerik Üretimi Eğitimi — Final Projesi  ·  Kurgusal marka"], 16, COP, False)

s = slide("Marka analizi ve rakipler")
ptable(s, ["Rakip", "Konumlandırma (genel)", "Fırsat boşluğu"], [list(c) for c in COMPETITORS], .6, 1.5, 12.1, 12, [2.6, 4.7, 4.8])
text(s, .6, 5.0, 12, 1, [COMP_NOTE], 11, SAGE, False)

s = slide("Marka kimliği kartı")
for i, (n, h, u) in enumerate(PALETTE):
    b = s.shapes.add_shape(1, Inches(.6 + i * 2.45), Inches(1.6), Inches(2.25), Inches(1.8)); b.fill.solid(); b.fill.fore_color.rgb = prgb(h); b.line.color.rgb = prgb(ESP)
    text(s, .7 + i * 2.45, 3.45, 2.2, 1, [f"{n}", h, u], 12, ESP, False)
text(s, .6, 4.9, 12, 2, [f"Değerler: {', '.join(VALUES)}", f"Slogan: {TAGLINE}", "Görsel dil: düz çizimler, bol boşluk, yalnızca 5 renk", "Yazı tipi: Georgia (başlık) + Segoe UI / Calibri (metin)"], 16)

s = slide("Neden – Kime – Ne – Nasıl")
text(s, .6, 1.5, 12.1, 5.5, [f"NEDEN: {WHY}", f"KİME: {WHO}", f"NE: {WHAT}", f"NASIL: {HOW}"], 15, ESP)

s = slide("Marka sesi rehberi")
text(s, .6, 1.5, 5.9, 4, ["YAP"] + TONE_DO, 15, SAGE); text(s, 6.8, 1.5, 6, 4, ["YAPMA"] + TONE_DONT, 15, COP)
text(s, .6, 5.5, 12, 1.2, [f"Tercih edilen sözcükler: {', '.join(VOCAB)}", f"Kaçınılan sözcükler: {', '.join(AVOID)}"], 14, ESP)

s = slide("İçerik sütunları")
ptable(s, ["Sütun", "İçerik", "Hedef kitleyle bağı"], [list(p) for p in PILLARS], .6, 1.6, 12.1, 13, [2.8, 5, 4.3])

s = slide("7 günlük içerik takvimi (16–22 Kasım 2026)")
ptable(s, ["Gün", "Saat", "Sütun", "Format", "Kanal", "Konu"], [[c[0] + " " + c[1][:5], c[2], c[3], c[4], c[5], c[6]] for c in CAL], .5, 1.5, 12.3, 11, [1.9, .8, 2.0, 2.2, 1.9, 3.5])
text(s, .5, 5.3, 12.3, 1.5, ["Gerekçeler ve marka sesi notları: 2_Icerik_Takvimi.xlsx dosyasında."], 12, SAGE, False)

s = slide("Örnek içerik 1 — Blog yazısı")
text(s, .6, 1.5, 12, 1, [BLOG_TITLE, f"Anahtar kelimeler: {BLOG_KEYWORDS}"], 17, ESP, False)
text(s, .6, 2.9, 12, 4, [BLOG[0][1].replace("**", ""), "5 adım: Oranı belirle · Taze öğüt · Suyun sıcaklığı · Yavaş ve daire çizerek dök · Tadı oku, ayarla", "Tam metin: icerik_seti/blog_yazisi.docx (≈450 kelime)"], 14)

s = slide("Örnek içerik 2 — Sosyal medya (RTF formülü)")
for i, p in enumerate(POSTS):
    text(s, .5 + i * 4.2, 1.5, 4.0, 5.4, [f"{p['kanal']} · {p['sutun']}"] + p["metin"].split("\n"), 11, ESP, False)

s = slide("Örnek içerik 3 — Görseller (marka paleti)")
for i, f in enumerate(("gorsel_1_marka_karti.png", "gorsel_2_demleme_orani.png", "gorsel_3_cifliktten_fincana.png")):
    from PIL import Image
    w_, h_ = Image.open(f"{S}/{f}").size; k = min(3.9 / w_, 5.3 / h_); ww, hh = w_ * k, h_ * k
    s.shapes.add_picture(f"{S}/{f}", Inches(.6 + i * 4.2 + (3.9 - ww) / 2), Inches(1.5), width=Inches(ww), height=Inches(hh))
text(s, .6, 6.9, 12, .4, ["Görseller Python (Pillow) ile marka paletine uygun olarak çizilmiştir."], 11, SAGE, False)

s = slide("Örnek içerik 4–5 — Video ve seslendirme")
for i in range(1, 5): s.shapes.add_picture(f"{S}/video_kare_{i}.png", Inches(.6 + (i - 1) * 2.3), Inches(1.5), height=Inches(4.0))
text(s, .6, 5.7, 12, 1.5, ["video_tanitim.mp4 — 18,6 sn, dikey 1080×1920, seslendirmeli", f"Seslendirme (tr-TR-EmelNeural): \"{VOICE}\"", "Dosyalar: icerik_seti/video_tanitim.mp4 ve seslendirme.mp3"], 12)

s = slide("İçerik kontrol listesi")
ptable(s, ["İçerik", "Marka sesi", "Telif / etik", "Halüsinasyon", "Aksiyon"], [[r[0], r[1], r[2], r[3], r[4]] for r in CHK[:6]], .4, 1.4, 12.5, 7, [1.5, 2.3, 3.0, 3.0, 2.7])

s = slide("AI kullanım raporu ve prompt kütüphanesi")
ptable(s, AI_HEAD, AI, .4, 1.4, 12.5, 9, [2.6, 2.3, 3.2, 4.4])
text(s, .4, 5.5, 12.5, 1.6, [f"{a}: {b[:150]}…" for a, b in PROMPTS[:2]], 10, ESP)
from contentflow import checker, report as rep
res = checker.tum_icerigi_kontrol(REPO / "content")
s = slide("Kontrol katmanı çıktısı (contentflow kontrol)")
ptable(s, ["İçerik", "Ton", "Anahtar kelime", "Telif", "Kaynak doğrulama", "Karar"], [[r.dosya, *[r.alan_durumu(a) for a in checker.ALANLAR], r.durum] for r in res], .4, 1.4, 12.5, 10, [3.6, 1.4, 1.9, 1.4, 2.3, 1.9])
text(s, .4, 5.9, 12.5, 1.2, ["Araç gerçek metni tarar; kaynakla doğrulanmamış teknik değerler 'ONAY_GEREKLİ' olarak işaretlenir. İnsan onayı olmadan kuyruğa alınmaz."], 12, SAGE, False)
s = slide("Otomasyon ve performans raporu (isteğe bağlı pratikler)")
text(s, .6, 1.5, 6, 5, ["Tetikleyici → eylem akışı: blog yayını → kontrol → kuyruk; ONAY_GEREKLİ → bildirim; Cuma 09:00 → haftalık rapor", "Gerçek Make/Zapier hesabına bağlı değildir; automation/scenarios.json tasarımı ve contentflow/automation.py yerel simülasyonu vardır", "Performans raporu SİMÜLE veriyle gösterilmiştir; gerçek sonuç değildir"], 14)
o = rep.ozet(rep.oku(REPO / "data" / "performans_simule.csv")); rep.grafik(o, REPO / "deliverables" / "icerik_seti" / "performans_simule.png")
s.shapes.add_picture(str(REPO / "deliverables" / "icerik_seti" / "performans_simule.png"), Inches(6.8), Inches(1.6), width=Inches(6))
prs.save(f"{O}/ContentFlow_Kivam_Kahve_Teslim_Sunumu.pptx")
print("ok")
