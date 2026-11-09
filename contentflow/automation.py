"""Tetikleyici–eylem akışının yerel simülasyonu (Make/Zapier mantığı).

Gerçek bir servise bağlanmaz: 'kuyruk' ve 'bildirim' çıktıları dosya olarak yazılır.
"""
from __future__ import annotations

import datetime as dt
import json
import pathlib

from . import checker, report


def planlanan_zaman(meta: dict) -> str | None:
    return meta.get("planlanan")


def onaylari_yukle(yol: pathlib.Path | None = None) -> dict:
    """İnsan onayları: {"dosya.md": {"onaylayan": "ad", "tarih": "YYYY-MM-DD", "kapsam": ["kaynak_dogrulama"]}}"""
    yol = yol or checker.ROOT / "brand" / "onaylar.json"
    return json.loads(pathlib.Path(yol).read_text(encoding="utf-8")) if pathlib.Path(yol).exists() else {}


def pipeline_calistir(icerik_klasoru: pathlib.Path, cikti: pathlib.Path, onaylar: dict | None = None) -> list[dict]:
    """Her içerik için kontrol çalıştırır; karara göre kuyruğa alır, onaya yollar veya reddeder.

    Uyarılar yalnızca ilgili alanı kapsayan, adı ve tarihi olan bir insan onayı varsa geçer.
    """
    onaylar = onaylari_yukle() if onaylar is None else onaylar
    icerik_klasoru, cikti = pathlib.Path(icerik_klasoru), pathlib.Path(cikti)
    for alt in ("queue", "notifications", "rejected"):
        (cikti / alt).mkdir(parents=True, exist_ok=True)
    marka = checker.marka_yukle()
    kararlar = []
    for yol in sorted(icerik_klasoru.rglob("*.md")):
        meta, govde = checker.icerik_oku(yol)
        s = checker.kontrol_et(yol, marka)
        kayit = {"dosya": yol.name, "kanal": meta.get("kanal"), "karar": s.durum, "planlanan": planlanan_zaman(meta)}
        if s.durum == "ONAY_GEREKLİ":
            o = onaylar.get(yol.name, {})
            uyari_alanlari = {b.alan for b in s.bulgular if b.seviye == "uyarı"}
            if o.get("onaylayan") and o.get("tarih") and uyari_alanlari <= set(o.get("kapsam", [])):
                kayit["karar"] = "GEÇTİ"
                kayit["onaylayan"] = o["onaylayan"]
        if kayit["karar"] == "GEÇTİ":
            if not kayit["planlanan"]:
                kayit["karar"] = "ONAY_GEREKLİ"
                kayit["neden"] = "planlanan zaman yok"
            else:
                (cikti / "queue" / f"{yol.stem}.json").write_text(json.dumps({"kanal": meta.get("kanal"), "zaman": kayit["planlanan"], "metin": govde}, ensure_ascii=False, indent=1), encoding="utf-8")
        if kayit["karar"] != "GEÇTİ":
            hedef = "rejected" if s.durum == "RED" else "notifications"
            satirlar = [f"[{b.seviye}] ({b.alan}) {b.mesaj}" for b in s.bulgular if b.seviye != "bilgi"]
            (cikti / hedef / f"{yol.stem}.txt").write_text(f"{yol.name}: {kayit['karar']}\n" + "\n".join(satirlar), encoding="utf-8")
        kararlar.append(kayit)
    (cikti / "kararlar.json").write_text(json.dumps(kararlar, ensure_ascii=False, indent=1), encoding="utf-8")
    return kararlar


def haftalik_rapor(veri_csv: pathlib.Path, cikti: pathlib.Path) -> pathlib.Path:
    cikti = pathlib.Path(cikti) / "reports"
    cikti.mkdir(parents=True, exist_ok=True)
    o = report.ozet(report.oku(veri_csv))
    md = cikti / "haftalik_rapor.md"
    md.write_text(report.markdown(o), encoding="utf-8")
    report.grafik(o, cikti / "haftalik_rapor.png")
    return md


def cuma_09_mu(an: dt.datetime) -> bool:
    """Haftalık rapor tetikleyicisi (cron: 0 9 * * 5)."""
    return an.weekday() == 4 and an.hour == 9 and an.minute == 0
