"""Komut satırı: python -m contentflow <komut>"""
from __future__ import annotations

import argparse
import pathlib
import sys

from . import automation, calendar_tool, checker, report

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="contentflow", description="Kıvam Kahve içerik üretim sistemi araçları")
    sub = ap.add_subparsers(dest="komut", required=True)
    c = sub.add_parser("kontrol", help="İçerik kontrol katmanı (ton, anahtar kelime, telif, kaynak)")
    c.add_argument("--icerik", default=str(ROOT / "content"))
    c.add_argument("--rapor", help="Markdown raporu yazılacak dosya")
    sub.add_parser("takvim", help="Takvimi doğrula ve Excel üret").add_argument("--cikti", default=str(ROOT / "out" / "icerik_takvimi.xlsx"))
    p = sub.add_parser("pipeline", help="Tetikleyici-eylem akışını simüle et")
    p.add_argument("--cikti", default=str(ROOT / "out"))
    r = sub.add_parser("rapor", help="Performans raporu (simüle veriyle)")
    r.add_argument("--veri", default=str(ROOT / "data" / "performans_simule.csv"))
    r.add_argument("--cikti", default=str(ROOT / "out"))
    a = ap.parse_args(argv)

    if a.komut == "kontrol":
        sonuc = checker.tum_icerigi_kontrol(pathlib.Path(a.icerik))
        md = checker.markdown_rapor(sonuc)
        if a.rapor:
            pathlib.Path(a.rapor).write_text(md, encoding="utf-8")
        print(md)
        return 1 if any(s.durum == "RED" for s in sonuc) else 0
    if a.komut == "takvim":
        t = calendar_tool.yukle()
        hatalar = calendar_tool.dogrula(t)
        if hatalar:
            print("\n".join("HATA: " + h for h in hatalar), file=sys.stderr)
            return 1
        pathlib.Path(a.cikti).parent.mkdir(parents=True, exist_ok=True)
        calendar_tool.excel_yaz(t, pathlib.Path(a.cikti))
        print("Takvim geçerli; yazıldı:", a.cikti)
        return 0
    if a.komut == "pipeline":
        for k in automation.pipeline_calistir(ROOT / "content", pathlib.Path(a.cikti)):
            print(f"{k['dosya']:<22} {k['kanal']:<10} {k['karar']:<14} {k.get('planlanan') or ''}")
        return 0
    if a.komut == "rapor":
        print("Yazıldı:", automation.haftalik_rapor(pathlib.Path(a.veri), pathlib.Path(a.cikti)))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
