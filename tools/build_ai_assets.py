"""Üretken yapay zeka görsellerinden teslim varlıklarını kurar.

Girdi : deliverables/icerik_seti/ai_adaylar/*.png  (tools/generate_ai_images.py çıktısı)
Çıktı : gorsel_1/2/3 (üretken görsel + marka metni bindirmesi), video_tanitim.mp4 (üretken görsellerden kurulmuş,
        yakınlaşma hareketi + altyazı + seslendirme), seslendirme.mp3, video_kare_*.png, assets.json
Not   : Videonun sahneleri üretken görsellerdir; hareket (yakınlaşma/geçiş) koddan gelir. Metinden-videoya model kullanılmamıştır.
"""
import asyncio
import json
import os
import pathlib
import subprocess

import edge_tts
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = ROOT / "deliverables" / "icerik_seti"
AD = S / "ai_adaylar"
ESP, CREMA, COP, SAGE, CREAM = "#3B2A20", "#E8D5B7", "#C8693A", "#7A8B6F", "#FAF6EF"
F = "C:/Windows/Fonts/"
H1 = lambda s: ImageFont.truetype(F + "georgiab.ttf", s)
BODY = lambda s: ImageFont.truetype(F + "segoeui.ttf", s)
BOLD = lambda s: ImageFont.truetype(F + "segoeuib.ttf", s)
# Seçilen adaylar (kontak sayfasından elle seçildi)
SECIM = {"g1": "gorsel1_marka_karti_3", "g2": "gorsel2_demleme_orani_1", "g3": "gorsel3_cifliktten_fincana_2",
         "v1": "video_sahne1_3", "v2": "video_sahne2_1", "v3": "video_sahne3_3"}


def cover(img: Image.Image, W: int, H: int) -> Image.Image:
    k = max(W / img.width, H / img.height)
    img = img.resize((int(img.width * k) + 1, int(img.height * k) + 1), Image.LANCZOS)
    x, y = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((x, y, x + W, y + H))


def ac(ad: str) -> Image.Image:
    return Image.open(AD / f"{ad}.png").convert("RGB")


def panel(im: Image.Image, box, renk=CREAM, alpha=232, r=36) -> Image.Image:
    kat = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(kat).rounded_rectangle(box, radius=r, fill=renk + format(alpha, "02x"))
    return Image.alpha_composite(im.convert("RGBA"), kat).convert("RGB")


def ortala(d, metin, y, font, renk, W, aralik=10):
    for satir in metin.split("\n"):
        d.text(((W - d.textlength(satir, font=font)) / 2, y), satir, font=font, fill=renk)
        y += font.size + aralik
    return y


def gorsel1(slogan: bool = True) -> Image.Image:
    im = cover(ac(SECIM["g1"]), 1080, 1350)
    if slogan:
        im = panel(im, (90, 1010, 990, 1290))
        d = ImageDraw.Draw(im)
        ortala(d, "Acele etme,\ntadına var.", 1030, H1(78), ESP, 1080, 6)
        d.text(((1080 - d.textlength("@kivamkahve", font=BOLD(32))) / 2, 1225), "@kivamkahve", font=BOLD(32), fill=COP)
    im = panel(im, (330, 40, 750, 120), ESP, 240, 40)
    d = ImageDraw.Draw(im)
    d.text(((1080 - d.textlength("KIVAM KAHVE", font=BOLD(36))) / 2, 58), "KIVAM KAHVE", font=BOLD(36), fill=CREMA)
    return im


def gorsel2() -> Image.Image:
    im = cover(ac(SECIM["g2"]), 1080, 1080)
    d = ImageDraw.Draw(im)
    ortala(d, "BAŞLANGIÇ ORANI", 50, BOLD(38), CREMA, 1080)
    ortala(d, "1 : 16", 100, H1(150), COP, 1080)
    ortala(d, "1 gram kahve için 16 gram su", 925, BODY(42), CREAM, 1080)
    ortala(d, "Kıvam Kahve", 1000, H1(34), CREMA, 1080)
    return im


def gorsel3() -> Image.Image:
    im = cover(ac(SECIM["g3"]), 1080, 1920)
    im = panel(im, (70, 60, 1010, 330))
    d = ImageDraw.Draw(im)
    ortala(d, "Çiftlikten\nfincana", 80, H1(92), ESP, 1080, 4)
    im = panel(im, (70, 1760, 1010, 1870))
    d = ImageDraw.Draw(im)
    ortala(d, "Kıvam Kahve · Acele etme, tadına var.", 1792, BOLD(36), ESP, 1080)
    return im


SCRIPT = ("Güne yavaş başla. Kıvam Kahve ile evde filtre kahve demlemek çok kolay. "
          "Bir gram kahveye on altı gram su. Suyu yavaşça dök, sabırla bekle. "
          "Kıvam Kahve. Acele etme, tadına var.")


async def tts(mp3: pathlib.Path):
    sinir = []
    com = edge_tts.Communicate(SCRIPT, "tr-TR-EmelNeural", rate="+0%", boundary="SentenceBoundary")
    with open(mp3, "wb") as f:
        async for ch in com.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "SentenceBoundary":
                sinir.append((ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]))
    return sinir


def sahne_tabanlari() -> list[Image.Image]:
    W, H = 1080, 1920
    s1 = gorsel1(slogan=False)   # altyazı alt bantta olduğu için sloganlı panel videoda yok
    t1 = Image.new("RGB", (W, H), ESP); t1.paste(cover(s1, W, H))
    s2 = cover(ac(SECIM["v1"]), W, H); s2 = panel(s2, (90, 70, 990, 250)); ImageDraw.Draw(s2)
    ortala(ImageDraw.Draw(s2), "Güne yavaş başla", 100, H1(80), ESP, W)
    s3 = Image.new("RGB", (W, H), ESP); s3.paste(gorsel2(), (0, 420))
    s4 = cover(ac(SECIM["v3"]), W, H); s4 = panel(s4, (90, 70, 990, 420))
    d = ImageDraw.Draw(s4)
    ortala(d, "Kıvam Kahve", 100, H1(96), ESP, W); ortala(d, "Acele etme, tadına var.", 235, BODY(46), COP, W); ortala(d, "@kivamkahve", 310, BOLD(40), ESP, W)
    return [t1, s2, s3, s4]


def main():
    W, H, FPS = 1080, 1920, 24
    g1, g2, g3 = gorsel1(), gorsel2(), gorsel3()
    g1.save(S / "gorsel_1_marka_karti.png"); g2.save(S / "gorsel_2_demleme_orani.png"); g3.save(S / "gorsel_3_cifliktten_fincana.png")
    mp3 = S / "seslendirme.mp3"
    sinir = asyncio.run(tts(mp3))
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    dur = float(subprocess.run([ff, "-i", str(mp3)], capture_output=True, text=True).stderr.split("Duration: ")[1].split(",")[0].split(":")[2])
    T = min(20.0, max(16.0, dur + 1.5))
    sahneler = [(0, 3.5), (3.5, 9.0), (9.0, 14.0), (14.0, T)]
    tabanlar = sahne_tabanlari()

    def kare(t: float) -> Image.Image:
        i = next((k for k, (a, b) in enumerate(sahneler) if a <= t < b), 3)
        a0, b0 = sahneler[i]
        z = 1.0 + 0.07 * (t - a0) / (b0 - a0)                      # yavaş yakınlaşma
        cw, ch = W / z, H / z
        x0, y0 = (W - cw) / 2, (H - ch) / 2
        im = tabanlar[i].resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))
        fade = min((t - a0) / .5, (b0 - t) / .5, 1)
        if fade < 1:
            im = Image.blend(Image.new("RGB", (W, H), ESP), im, max(0, fade))
        cumle = next((m for a, b, m in sinir if a - .05 <= t <= b + .15), None)
        if cumle:
            d = ImageDraw.Draw(im); satirlar, cur = [], ""
            for w_ in cumle.split():
                if d.textlength((cur + " " + w_).strip(), font=BOLD(46)) > 940: satirlar.append(cur); cur = w_
                else: cur = (cur + " " + w_).strip()
            satirlar.append(cur); top = 1700 - 30
            im = panel(im, (60, top - 20, 1020, top + len(satirlar) * 60 + 20), ESP, 235, 24); d = ImageDraw.Draw(im)
            for k, ln in enumerate(satirlar): d.text(((W - d.textlength(ln, font=BOLD(46))) / 2, top + k * 60), ln, font=BOLD(46), fill=CREAM)
        return im

    tmp = S / "_tmp_video.mp4"
    w = imageio_ffmpeg.write_frames(str(tmp), (W, H), fps=FPS, macro_block_size=1, codec="libx264", pix_fmt_in="rgb24", pix_fmt_out="yuv420p", output_params=["-crf", "22"])
    w.send(None)
    for n in range(int(T * FPS)):
        w.send(np.array(kare(n / FPS)).tobytes())
    w.close()
    subprocess.run([ff, "-y", "-i", str(tmp), "-i", str(mp3), "-c:v", "copy", "-c:a", "aac", "-af", "apad", "-t", str(T), str(S / "video_tanitim.mp4")], capture_output=True)
    os.remove(tmp)
    for k, t in enumerate((1.5, 6, 11, T - 1.5), 1):
        kare(t).resize((540, 960)).save(S / f"video_kare_{k}.png")

    istemler = json.loads((AD / "prompts.json").read_text(encoding="utf-8"))
    ref = lambda ad: istemler[ad + ".png"]
    LIS = "FLUX.1-schnell: Apache-2.0; SDXL-Lightning: CreativeML OpenRAIL++-M (model kartlarına göre)"
    assets = [
        {"dosya": "gorsel_1_marka_karti.png", "kaynak": f"Üretken YZ: Cloudflare Workers AI, {ref(SECIM['g1'])['model']}; marka metni Python ile bindirildi", "lisans": LIS, "uretim_yontemi": "tools/generate_ai_images.py + tools/build_ai_assets.py", "yapay_zeka_notu": "Görsel üretken yapay zeka çıktısıdır (istem: ai_adaylar/prompts.json); sanatçı/marka adı kullanılmadı"},
        {"dosya": "gorsel_2_demleme_orani.png", "kaynak": f"Üretken YZ: Cloudflare Workers AI, {ref(SECIM['g2'])['model']}; metin Python ile bindirildi", "lisans": LIS, "uretim_yontemi": "tools/generate_ai_images.py + tools/build_ai_assets.py", "yapay_zeka_notu": "Görsel üretken yapay zeka çıktısıdır; sanatçı/marka adı kullanılmadı"},
        {"dosya": "gorsel_3_cifliktten_fincana.png", "kaynak": f"Üretken YZ: Cloudflare Workers AI, {ref(SECIM['g3'])['model']}; metin Python ile bindirildi", "lisans": LIS, "uretim_yontemi": "tools/generate_ai_images.py + tools/build_ai_assets.py", "yapay_zeka_notu": "Görsel üretken yapay zeka çıktısıdır; sanatçı/marka adı kullanılmadı"},
        {"dosya": "video_tanitim.mp4", "kaynak": "Üretken YZ görsellerinden kurulmuş video (yakınlaşma hareketi ve geçişler Python/ffmpeg ile); altyazı ve yapay seslendirme", "lisans": LIS + "; müzik yok", "uretim_yontemi": "tools/build_ai_assets.py", "yapay_zeka_notu": "Metinden-videoya modeli kullanılmadı; sahneler üretken görseldir, hareket koddan gelir"},
        {"dosya": "seslendirme.mp3", "kaynak": "edge-tts (Microsoft Edge Türkçe nöral ses, tr-TR-EmelNeural)", "lisans": "Microsoft Edge okuma servisi; ticari kullanım koşulları yayından önce kontrol edilmelidir", "uretim_yontemi": "tools/build_ai_assets.py", "yapay_zeka_notu": "Yapay ses; gerçek kişi sesi taklit edilmedi"},
    ]
    (ROOT / "content" / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2), encoding="utf-8")
    print("tamam, video süresi", T)


if __name__ == "__main__":
    main()
