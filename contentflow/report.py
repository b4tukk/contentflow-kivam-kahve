"""Performans raporlama servisi (isteğe bağlı pratik 3).

ÖNEMLİ: Bu depoda gerçek yayın verisi yoktur. `data/performans_simule.csv` SİMÜLE edilmiş örnek veridir
(simule=true). Rapor biçimini ve hesaplamayı göstermek içindir; gerçek etkileşim sonuçları olarak sunulmamalıdır.
"""
from __future__ import annotations

import csv
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALANLAR = ["tarih", "kanal", "icerik", "goruntulenme", "begeni", "yorum", "paylasim", "simule"]


def simule_veri_uret(yol: pathlib.Path, tohum: int = 7) -> None:
    rnd = random.Random(tohum)
    satirlar = [
        ("2026-11-16", "web", "Blog: evde filtre kahve", (800, 1400)),
        ("2026-11-17", "instagram", "1:16 oranı gönderisi", (1500, 3000)),
        ("2026-11-18", "instagram", "Çiftlikten fincana (story)", (900, 1800)),
        ("2026-11-19", "instagram", "Video: Güne yavaş başla", (3000, 7000)),
        ("2026-11-20", "linkedin", "Günün ortasında 5 dakika", (600, 1500)),
        ("2026-11-21", "x", "1:15 mi 1:17 mi?", (400, 1200)),
        ("2026-11-22", "instagram", "Topluluk sorusu (story)", (700, 1500)),
    ]
    with open(yol, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(ALANLAR)
        for tarih, kanal, icerik, (lo, hi) in satirlar:
            g = rnd.randint(lo, hi)
            w.writerow([tarih, kanal, icerik, g, int(g * rnd.uniform(.03, .09)), int(g * rnd.uniform(.002, .012)), int(g * rnd.uniform(.003, .02)), "true"])


def oku(yol: pathlib.Path) -> list[dict]:
    with open(yol, newline="", encoding="utf-8") as f:
        satirlar = list(csv.DictReader(f))
    for s in satirlar:
        for k in ("goruntulenme", "begeni", "yorum", "paylasim"):
            s[k] = int(s[k])
        if s["goruntulenme"] < 0:
            raise ValueError("Negatif görüntülenme")
    return satirlar


def etkilesim_orani(s: dict) -> float:
    return (s["begeni"] + s["yorum"] + s["paylasim"]) / s["goruntulenme"] if s["goruntulenme"] else 0.0


def ozet(satirlar: list[dict]) -> dict:
    kanal: dict[str, dict] = {}
    for s in satirlar:
        k = kanal.setdefault(s["kanal"], {"goruntulenme": 0, "etkilesim": 0, "icerik": 0})
        k["goruntulenme"] += s["goruntulenme"]
        k["etkilesim"] += s["begeni"] + s["yorum"] + s["paylasim"]
        k["icerik"] += 1
    for k in kanal.values():
        k["oran"] = k["etkilesim"] / k["goruntulenme"] if k["goruntulenme"] else 0.0
    en_iyi = max(satirlar, key=etkilesim_orani) if satirlar else None
    toplam_g = sum(s["goruntulenme"] for s in satirlar)
    toplam_e = sum(s["begeni"] + s["yorum"] + s["paylasim"] for s in satirlar)
    return {"kanal": kanal, "toplam_goruntulenme": toplam_g, "toplam_etkilesim": toplam_e, "genel_oran": toplam_e / toplam_g if toplam_g else 0.0,
            "en_iyi": en_iyi["icerik"] if en_iyi else None, "simule": all(s["simule"] == "true" for s in satirlar)}


def markdown(o: dict) -> str:
    uyari = "> ⚠️ **SİMÜLE VERİ:** Aşağıdaki sayılar gerçek yayın sonucu değil, biçimi göstermek için üretilmiş örnek veridir.\n\n" if o["simule"] else ""
    sat = ["# Haftalık Performans Raporu", "", uyari + f"Toplam görüntülenme: **{o['toplam_goruntulenme']:,}** · Toplam etkileşim: **{o['toplam_etkilesim']:,}** · Genel etkileşim oranı: **%{o['genel_oran']*100:.1f}**".replace(",", "."), "",
           f"En yüksek etkileşim oranlı içerik: **{o['en_iyi']}**", "", "| Kanal | İçerik | Görüntülenme | Etkileşim | Oran |", "|---|---|---|---|---|"]
    for k, v in sorted(o["kanal"].items(), key=lambda kv: -kv[1]["goruntulenme"]):
        sat.append(f"| {k} | {v['icerik']} | {v['goruntulenme']} | {v['etkilesim']} | %{v['oran']*100:.1f} |")
    return "\n".join(sat) + "\n"


def grafik(o: dict, yol: pathlib.Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    kanallar = sorted(o["kanal"], key=lambda k: -o["kanal"][k]["goruntulenme"])
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.bar(kanallar, [o["kanal"][k]["goruntulenme"] for k in kanallar], color="#C8693A")
    ax.set_title("Kanal bazlı görüntülenme" + (" (SİMÜLE VERİ)" if o["simule"] else ""))
    ax.set_ylabel("Görüntülenme")
    fig.tight_layout()
    fig.savefig(yol, dpi=150)
    plt.close(fig)
