"""Üretken yapay zeka ile görsel üretimi (Cloudflare Workers AI: FLUX.1-schnell ve SDXL-Lightning).

Anahtarlar `.env` dosyasından okunur (CF_ACCOUNT_ID, CF_API_TOKEN); dosya git'e girmez, ekrana yazdırılmaz.
Kullanım: python tools/generate_ai_images.py [aday_sayisi] [istem_adı ...]
Çıktı: deliverables/icerik_seti/ai_adaylar/<ad>_<tohum>.png ve prompts.json (kullanılan istemler ve model)
"""
import base64
import io
import json
import pathlib
import re
import sys
import time

import requests
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverables" / "icerik_seti" / "ai_adaylar"
FLUX = "@cf/black-forest-labs/flux-1-schnell"
SDXL = "@cf/bytedance/stable-diffusion-xl-lightning"
NEG = "text, letters, words, numbers, watermark, logo, people, faces, hands, blurry, photo, realistic"

# istem adı -> (istem, genişlik, yükseklik, model). Palet sözcükle anlatılır; yazı, insan, marka/sanatçı adı yoktur.
ISTEMLER = {
    "gorsel1_marka_karti": ("Minimal flat vector illustration of a pour-over coffee dripper on a small glass carafe with three soft steam lines, "
                            "warm earthy palette: dark espresso brown, cream background, copper orange dripper, sage green steam, "
                            "lots of empty space at the bottom, calm cozy mood, vertical poster composition, no text, no people", 832, 1024, SDXL),
    "gorsel2_demleme_orani": ("Top-down flat vector illustration of a small kitchen scale with a coffee dripper and a measuring jug, "
                              "dark espresso brown background, cream and copper orange accents, clean geometric shapes, minimal, "
                              "empty space at the top, square composition, no text, no numbers, no people", 1024, 1024, FLUX),
    "gorsel3_cifliktten_fincana": ("Vertical flat vector illustration of the coffee journey from farm to cup: coffee cherry branch, roasting drum, "
                                   "pour-over brewing, two cups on a table, connected by a thin sage green line, cream beige background, "
                                   "espresso brown and copper orange accents, minimal, calm, generous empty space at the top, no text, no people", 576, 1024, SDXL),
    "video_sahne1": ("Flat vector illustration, close view of a pour-over coffee dripper with water slowly dripping into a glass carafe, soft steam, "
                     "warm palette of espresso brown, cream and copper orange, minimal background, vertical composition, no text, no people", 576, 1024, SDXL),
    "video_sahne2": ("Flat vector illustration of a ceramic cup of coffee on a wooden table next to a small kitchen scale and a gooseneck kettle, "
                     "morning light, warm palette of espresso brown, cream and copper orange, minimal, vertical composition, no text, no people", 576, 1024, SDXL),
    "video_sahne3": ("Flat vector illustration of two coffee cups and a small plant on a window sill, calm morning mood, "
                     "warm palette of espresso brown, cream and sage green, minimal, vertical composition, empty space at the top, no text, no people", 576, 1024, SDXL),
}


def anahtarlar() -> tuple[str, str]:
    t = (ROOT / ".env").read_text(encoding="utf-8")
    a, k = re.search(r"CF_ACCOUNT_ID\s*=\s*(\S+)", t), re.search(r"CF_API_TOKEN\s*=\s*(\S+)", t)
    if not (a and k):
        raise SystemExit(".env içinde CF_ACCOUNT_ID ve CF_API_TOKEN olmalı")
    return a.group(1), k.group(1)


def uret(hesap: str, tok: str, model: str, istem: str, w: int, h: int, tohum: int) -> Image.Image:
    govde = {"prompt": istem}
    if model == FLUX:
        govde["steps"] = 6          # FLUX uç noktası seed kabul etmez; her çağrı farklı sonuç verir
    else:
        govde.update(seed=tohum, negative_prompt=NEG, width=w, height=h, num_steps=8, guidance=2.0)
    r = requests.post(f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{model}", headers={"Authorization": f"Bearer {tok}"}, json=govde, timeout=180)
    r.raise_for_status()
    if r.headers.get("content-type", "").startswith("image/"):
        return Image.open(io.BytesIO(r.content)).convert("RGB")
    return Image.open(io.BytesIO(base64.b64decode(r.json()["result"]["image"]))).convert("RGB")


def main(n: int = 2, secilen: list[str] | None = None) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    hesap, tok = anahtarlar()
    yol = OUT / "prompts.json"
    kayit = json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else {}
    for ad, (istem, w, h, model) in ISTEMLER.items():
        if secilen and ad not in secilen:
            continue
        for tohum in range(1, n + 1):
            hedef = OUT / f"{ad}_{tohum}.png"
            if hedef.exists():
                continue
            try:
                img = uret(hesap, tok, model, istem, w, h, tohum)
                img.save(hedef)
                kayit[hedef.name] = {"istem": istem, "model": model.split("/")[-1], "boyut": list(img.size)}
                print("tamam", hedef.name, img.size)
            except requests.HTTPError as e:
                print("HATA", hedef.name, e.response.status_code, e.response.text[:140].replace("\n", " "))
                if e.response.status_code in (401, 403, 429):
                    yol.write_text(json.dumps(kayit, ensure_ascii=False, indent=1), encoding="utf-8")
                    raise SystemExit("Yetki/kota hatası; durduruldu.")
            time.sleep(1)
    yol.write_text(json.dumps(kayit, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2, sys.argv[2:] or None)
