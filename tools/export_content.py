"""content_source.py içindeki metinleri content/ klasörüne Markdown (front matter'lı) olarak yazar."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import content_source as cs  # noqa: E402

(ROOT / "content" / "posts").mkdir(parents=True, exist_ok=True)

body = [f"# {cs.BLOG_TITLE}\n"]
for kind, txt in cs.BLOG:
    body.append(f"## {txt}\n" if kind == "h" else txt.replace("**", "") + "\n")
(ROOT / "content" / "blog.md").write_text(
    f"---\ntur: blog\nkanal: web\nbaslik: {cs.BLOG_TITLE}\nmeta: {cs.BLOG_META}\nanahtar_kelime: evde filtre kahve\nplanlanan: 2026-11-16 09:00\n---\n" + "\n".join(body),
    encoding="utf-8",
)

kanal_slug = {"Instagram": "instagram", "X (Twitter)": "x", "LinkedIn": "linkedin"}
plan = {"Instagram": "2026-11-17 12:30", "X (Twitter)": "2026-11-21 11:00", "LinkedIn": "2026-11-20 09:30"}
for i, p in enumerate(cs.POSTS, 1):
    slug = kanal_slug[p["kanal"]]
    (ROOT / "content" / "posts" / f"{i:02d}_{slug}.md").write_text(
        f"---\ntur: sosyal\nkanal: {slug}\nsutun: {p['sutun']}\ngorsel: {p['gorsel'] or ''}\nplanlanan: {plan[p['kanal']]}\nrtf_istemi: {p['rtf']}\n---\n{p['metin']}\n",
        encoding="utf-8",
    )

assets = [
    {"dosya": f, "kaynak": "Python (Pillow) ile kodla çizildi", "lisans": "Özgün; yazı tipleri sistem fontları (Georgia, Segoe UI)", "uretim_yontemi": "tools/generate_media.py", "yapay_zeka_notu": "Üretken görsel YZ kullanılmadı; çizimi kod üretti, kodu Claude yazdı"}
    for f in ("gorsel_1_marka_karti.png", "gorsel_2_demleme_orani.png", "gorsel_3_cifliktten_fincana.png")
] + [
    {"dosya": "video_tanitim.mp4", "kaynak": "Python + ffmpeg (imageio-ffmpeg)", "lisans": "Özgün; müzik yok", "uretim_yontemi": "tools/generate_media.py", "yapay_zeka_notu": "Kare kare kodla çizildi; seslendirme yapay ses"},
    {"dosya": "seslendirme.mp3", "kaynak": "edge-tts (Microsoft Edge Türkçe nöral ses, tr-TR-EmelNeural)", "lisans": "Ticari kullanım koşulları doğrulanmalı", "uretim_yontemi": "tools/generate_media.py", "yapay_zeka_notu": "Yapay ses; gerçek kişi sesi taklit edilmedi"},
]
(ROOT / "content" / "assets.json").write_text(json.dumps(assets, ensure_ascii=False, indent=2), encoding="utf-8")
print("içerik yazıldı")
