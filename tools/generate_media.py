import asyncio, math, os, subprocess, wave
from PIL import Image, ImageDraw, ImageFont
import numpy as np, imageio_ffmpeg, edge_tts

import pathlib
OUT = str(pathlib.Path(__file__).resolve().parent.parent / "deliverables")
os.makedirs(f"{OUT}/icerik_seti", exist_ok=True)
ESP, CREMA, COP, SAGE, CREAM = "#3B2A20", "#E8D5B7", "#C8693A", "#7A8B6F", "#FAF6EF"
F = "C:/Windows/Fonts/"
def font(name, size): return ImageFont.truetype(F + name, size)
H1 = lambda s: font("georgiab.ttf", s)
BODY = lambda s: font("segoeui.ttf", s)
BOLD = lambda s: font("segoeuib.ttf", s)

def center(d, text, y, fnt, fill, W, spacing=10):
    for line in text.split("\n"):
        w = d.textlength(line, font=fnt)
        d.text(((W - w) / 2, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y

def dripper(d, cx, cy, s=1.0, fill_level=0.0, drop_phase=None):
    """Sade bir pour-over çizimi. cx,cy: dripper'ın üst orta noktası."""
    w, h = 300 * s, 220 * s
    d.polygon([(cx - w / 2, cy), (cx + w / 2, cy), (cx + 55 * s, cy + h), (cx - 55 * s, cy + h)], fill=COP)
    d.rectangle([cx - 70 * s, cy + h, cx + 70 * s, cy + h + 22 * s], fill=ESP)
    # sürahi
    top = cy + h + 22 * s
    d.rounded_rectangle([cx - 120 * s, top, cx + 120 * s, top + 230 * s], radius=int(30 * s), fill=CREMA, outline=ESP, width=int(8 * s))
    if fill_level > 0:
        lv = 200 * s * fill_level
        d.rounded_rectangle([cx - 112 * s, top + 222 * s - lv, cx + 112 * s, top + 222 * s], radius=int(24 * s), fill=ESP)
    if drop_phase is not None:
        for k in range(2):
            t = (drop_phase + k * .5) % 1
            y = cy + h + 22 * s + t * 120 * s
            d.ellipse([cx - 7 * s, y, cx + 7 * s, y + 18 * s], fill=ESP)

def steam(d, cx, cy, t, s=1.0):
    for i, dx in enumerate((-60, 0, 60)):
        pts = [(cx + dx * s + math.sin(t * 2 + i + j / 3) * 14 * s, cy - j * 14 * s) for j in range(8)]
        d.line(pts, fill=SAGE, width=int(7 * s), joint="curve")

def base(W, Hh, bg=CREAM):
    im = Image.new("RGB", (W, Hh), bg); return im, ImageDraw.Draw(im)

# ---------------- GÖRSELLER ----------------
# 1) Marka kartı 1080x1350
im, d = base(1080, 1350)
d.rectangle([0, 0, 1080, 90], fill=ESP)
center(d, "KIVAM KAHVE", 22, BOLD(40), CREMA, 1080)
dripper(d, 540, 330, 1.0, fill_level=.45)
steam(d, 540, 290, 0.5, 1.0)
center(d, "Acele etme,\ntadına var.", 880, H1(92), ESP, 1080, 14)
d.rectangle([440, 1130, 640, 1136], fill=COP)
center(d, "Evde filtre kahve için sakin bir rehber", 1170, BODY(38), ESP, 1080)
center(d, "@kivamkahve", 1260, BOLD(34), COP, 1080)
im.save(f"{OUT}/icerik_seti/gorsel_1_marka_karti.png")

# 2) Demleme oranı 1080x1080
im, d = base(1080, 1080, ESP)
center(d, "BAŞLANGIÇ ORANI", 90, BOLD(40), CREMA, 1080)
center(d, "1 : 16", 170, H1(240), COP, 1080)
center(d, "1 gram kahve için 16 gram su", 480, BODY(46), CREAM, 1080)
steps = [("1", "Kahveyi tazece öğüt"), ("2", "Filtreyi ılık suyla ıslat"), ("3", "Suyu yavaş ve daire çizerek dök"), ("4", "Tadı sevmediysen oranı biraz değiştir")]
y = 600
for n, t in steps:
    d.ellipse([140, y, 210, y + 70], fill=COP); d.text((165, y + 10), n, font=BOLD(40), fill=CREAM)
    d.text((240, y + 12), t, font=BODY(40), fill=CREAM); y += 100
center(d, "Kıvam Kahve", 1000, H1(36), CREMA, 1080)
im.save(f"{OUT}/icerik_seti/gorsel_2_demleme_orani.png")

# 3) Hikâye 1080x1920
im, d = base(1080, 1920, CREMA)
center(d, "ÇİFTLİKTEN\nFİNCANA", 150, H1(110), ESP, 1080, 10)
d.rectangle([480, 440, 600, 446], fill=COP)
items = [("Hasat", "Olgun taneler elle toplanır"), ("Kavurma", "Tane, kendi tadını bulana kadar"), ("Demleme", "Sakin, ölçülü, sabırlı"), ("Paylaşım", "Bir fincan, iki sohbet")]
y = 560
for i, (a, b) in enumerate(items):
    d.line([(160, y + 40), (160, y + 250)], fill=SAGE, width=6) if i < 3 else None
    d.ellipse([125, y, 195, y + 70], fill=COP if i % 2 == 0 else ESP)
    d.text((240, y - 6), a, font=H1(60), fill=ESP)
    d.text((240, y + 64), b, font=BODY(38), fill=ESP)
    y += 260
center(d, "Kıvam Kahve · Acele etme, tadına var.", 1740, BOLD(36), ESP, 1080)
im.save(f"{OUT}/icerik_seti/gorsel_3_cifliktten_fincana.png")

# ---------------- SESLENDİRME ----------------
SCRIPT = ("Güne yavaş başla. Kıvam Kahve ile evde filtre kahve demlemek çok kolay. "
          "Bir gram kahveye on altı gram su. Suyu yavaşça dök, sabırla bekle. "
          "Kıvam Kahve. Acele etme, tadına var.")
open(f"{OUT}/icerik_seti/seslendirme_metni.txt", "w", encoding="utf8").write(SCRIPT)
mp3 = f"{OUT}/icerik_seti/seslendirme.mp3"
ALTYAZI = []   # (başlangıç sn, bitiş sn, metin) — cümle sınırlarından
async def tts():
    com = edge_tts.Communicate(SCRIPT, "tr-TR-EmelNeural", rate="+0%", boundary="SentenceBoundary")
    with open(mp3, "wb") as f:
        async for ch in com.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "SentenceBoundary": ALTYAZI.append((ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]))
asyncio.run(tts())
print("altyazı cümleleri:", len(ALTYAZI))
ff = imageio_ffmpeg.get_ffmpeg_exe()
dur = float(subprocess.run([ff, "-i", mp3], capture_output=True, text=True).stderr.split("Duration: ")[1].split(",")[0].split(":")[2])
print("ses süresi", dur)
T = min(20.0, max(16.0, dur + 1.5))

# ---------------- VİDEO ----------------
W, Hh, FPS = 1080, 1920, 24
n_frames = int(T * FPS)
scenes = [(0, 3.5), (3.5, 9.0), (9.0, 14.0), (14.0, T)]
def alpha_blend(img, bg_color, a):
    return Image.blend(Image.new("RGB", img.size, bg_color), img, max(0, min(1, a)))

def frame(t):
    s = next(i for i, (a, b) in enumerate(scenes) if a <= t < b) if t < T else 3
    a0, b0 = scenes[s]
    fade = min((t - a0) / .5, (b0 - t) / .5, 1)
    bg = ESP if s in (0, 2) else CREAM
    im, d = base(W, Hh, bg)
    lt = t - a0
    if s == 0:
        center(d, "KIVAM", 700, H1(150), CREMA, W); center(d, "KAHVE", 860, H1(150), COP, W)
        center(d, "Acele etme, tadına var.", 1100, BODY(48), CREAM, W)
    elif s == 1:
        center(d, "Güne yavaş başla", 230, H1(86), ESP, W)
        dripper(d, 540, 600, 1.6, fill_level=min(.8, lt / (b0 - a0)), drop_phase=(lt * 1.2) % 1)
        steam(d, 540, 560, lt, 1.4)
        center(d, "Suyu yavaşça dök,\nsabırla bekle.", 1450, BODY(60), ESP, W)
    elif s == 2:
        center(d, "BAŞLANGIÇ ORANI", 480, BOLD(44), CREMA, W)
        center(d, "1 : 16", 600, H1(260), COP, W)
        center(d, "1 gram kahve\n16 gram su", 960, BODY(62), CREAM, W)
    else:
        dripper(d, 540, 420, 1.2, fill_level=.8); steam(d, 540, 370, lt, 1.2)
        center(d, "Kıvam Kahve", 1150, H1(110), ESP, W)
        center(d, "Acele etme, tadına var.", 1320, BODY(52), COP, W)
        center(d, "@kivamkahve", 1450, BOLD(44), ESP, W)
    im = alpha_blend(im, bg, fade) if fade < 1 else im
    cumle = next((m for a, b, m in ALTYAZI if a - .05 <= t <= b + .15), None)
    if cumle:                                            # yakıştırılmış altyazı (alt bant)
        d = ImageDraw.Draw(im); words = cumle.split(); lines, cur = [], ""
        for wd in words:
            if d.textlength((cur + " " + wd).strip(), font=BOLD(46)) > 940: lines.append(cur); cur = wd
            else: cur = (cur + " " + wd).strip()
        lines.append(cur); top = 1700 - 30
        d.rounded_rectangle([60, top - 20, 1020, top + len(lines) * 60 + 20], radius=24, fill=ESP)
        for i, ln in enumerate(lines): d.text(((1080 - d.textlength(ln, font=BOLD(46))) / 2, top + i * 60), ln, font=BOLD(46), fill=CREAM)
    return im

vid_noaudio = f"{OUT}/icerik_seti/_tmp_video.mp4"
w = imageio_ffmpeg.write_frames(vid_noaudio, (W, Hh), fps=FPS, macro_block_size=1, codec="libx264", pix_fmt_in="rgb24", pix_fmt_out="yuv420p", output_params=["-crf", "23"])
w.send(None)
for i in range(n_frames):
    w.send(np.array(frame(i / FPS)).tobytes())
w.close()
final = f"{OUT}/icerik_seti/video_tanitim.mp4"
subprocess.run([ff, "-y", "-i", vid_noaudio, "-i", mp3, "-c:v", "copy", "-c:a", "aac", "-af", "apad", "-t", str(T), final], capture_output=True)
os.remove(vid_noaudio)
# kareler (ekran görüntüsü kanıtı)
for k, t in enumerate((1.5, 6, 11, T - 1.5), 1):
    frame(t).resize((540, 960)).save(f"{OUT}/icerik_seti/video_kare_{k}.png")
print("video", T, "sn", os.path.getsize(final) // 1024, "KB")
