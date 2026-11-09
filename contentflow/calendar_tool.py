"""7 günlük içerik takvimini doğrular ve Excel'e yazar."""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import re

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASLIK = ["Gün", "Tarih", "Saat", "İçerik sütunu", "Format", "Kanal", "Konu", "Gerekçe (hedef kitle bağlantısı)", "Marka sesi notu", "Üretim", "Dosya", "Durum"]
ANAHTAR = ["gun", "tarih", "saat", "sutun", "format", "kanal", "konu", "gerekce", "ses_notu", "uretim", "dosya", "durum"]
SUTUNLAR = {"Demleme Rehberi", "Çiftlikten Fincana", "Mola Anları", "Küçük Denemeler"}
GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]


def yukle(yol: pathlib.Path | None = None) -> list[dict]:
    return json.loads((yol or ROOT / "calendar" / "icerik_takvimi.json").read_text(encoding="utf-8"))


def dogrula(takvim: list[dict]) -> list[str]:
    """Hata mesajları listesi döner (boşsa takvim geçerlidir)."""
    hatalar: list[str] = []
    if len(takvim) != 7:
        hatalar.append(f"Takvim 7 gün olmalı (bulunan: {len(takvim)})")
    tarihler = []
    for i, r in enumerate(takvim, 1):
        eksik = [k for k in ANAHTAR if not str(r.get(k, "")).strip()]
        if eksik:
            hatalar.append(f"Satır {i}: eksik alan {eksik}")
            continue
        if r["sutun"] not in SUTUNLAR:
            hatalar.append(f"Satır {i}: bilinmeyen içerik sütunu '{r['sutun']}'")
        if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", r["saat"]):
            hatalar.append(f"Satır {i}: saat biçimi HH:MM olmalı ('{r['saat']}')")
        try:
            t = dt.datetime.strptime(r["tarih"], "%d.%m.%Y").date()
            tarihler.append(t)
            if r["gun"] != GUNLER[t.weekday()]:
                hatalar.append(f"Satır {i}: {r['tarih']} tarihi {GUNLER[t.weekday()]} günüdür, takvimde '{r['gun']}' yazıyor")
        except ValueError:
            hatalar.append(f"Satır {i}: tarih biçimi GG.AA.YYYY olmalı ('{r['tarih']}')")
    if len(tarihler) == 7:
        if sorted(tarihler) != tarihler or any((b - a).days != 1 for a, b in zip(tarihler, tarihler[1:])):
            hatalar.append("Tarihler ardışık 7 gün olmalı")
    kapsanan = {r.get("sutun") for r in takvim}
    if len(kapsanan & SUTUNLAR) < 3:
        hatalar.append("En az 3 farklı içerik sütunu kullanılmalı")
    return hatalar


def excel_yaz(takvim: list[dict], yol: pathlib.Path) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "7 Günlük Takvim"
    ws.append(BASLIK)
    for r in takvim:
        ws.append([r[k] for k in ANAHTAR])
    for c in ws[1]:
        c.font = Font(bold=True, color="FAF6EF")
        c.fill = PatternFill("solid", fgColor="3B2A20")
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    for col, w in zip("ABCDEFGHIJKL", (11, 11, 7, 16, 18, 16, 28, 42, 20, 20, 24, 9)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    wb.save(yol)
