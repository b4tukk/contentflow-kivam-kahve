import datetime as dt
import json
import pathlib

import pytest

from contentflow import automation, calendar_tool, checker, report

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARKA = checker.marka_yukle()


def yaz(tmp_path, ad, meta, govde):
    p = tmp_path / ad
    p.write_text("---\n" + "\n".join(f"{k}: {v}" for k, v in meta.items()) + "\n---\n" + govde, encoding="utf-8")
    return p


def alanlar(sonuc, seviye):
    return {b.alan for b in sonuc.bulgular if b.seviye == seviye}


# ---------- ton ----------
def test_slogan_acele_etme_izinli(tmp_path):
    s = checker.kontrol_et(yaz(tmp_path, "a.md", {"kanal": "instagram"}, "Bu hafta bir fincan demle. Acele etme, tadına var."))
    assert "ton_tutarliligi" not in alanlar(s, "hata")


@pytest.mark.parametrize("kelime", ["en iyi", "mucize", "kusursuz", "hızlı çözüm", "hack"])
def test_abartili_ve_yasakli_sozcuk_reddedilir(tmp_path, kelime):
    s = checker.kontrol_et(yaz(tmp_path, "a.md", {"kanal": "instagram"}, f"Dünyanın {kelime} kahvesini demle."))
    assert s.durum == "RED" and "ton_tutarliligi" in alanlar(s, "hata")


def test_fazla_unlem_uyari(tmp_path):
    s = checker.kontrol_et(yaz(tmp_path, "a.md", {"kanal": "instagram"}, "Kahve demle! Harika! Mola ver!"))
    assert any("ünlem" in b.mesaj for b in s.bulgular)


def test_kanal_hitap_istisnasi(tmp_path):
    siz = "Günün hangi anında yavaşlıyorsunuz? Sizi yorumlarda duymak isteriz. Fincan mola."
    assert any("'siz'" in b.mesaj for b in checker.kontrol_et(yaz(tmp_path, "a.md", {"kanal": "instagram"}, siz)).bulgular)
    assert not any("'siz'" in b.mesaj for b in checker.kontrol_et(yaz(tmp_path, "b.md", {"kanal": "linkedin"}, siz)).bulgular)


def test_x_karakter_siniri(tmp_path):
    s = checker.kontrol_et(yaz(tmp_path, "x.md", {"kanal": "x"}, "kahve demle " * 40))
    assert any("karakter sınırı" in b.mesaj for b in s.bulgular)


# ---------- anahtar kelime ----------
def blog(tmp_path, **kw):
    meta = {"tur": "blog", "kanal": "web", "baslik": "Evde Filtre Kahve Nasıl Demlenir", "meta": "Evde filtre kahve demlemek için sakin ve ölçülü bir rehber; oran, öğütme ve su sıcaklığı.", "anahtar_kelime": "evde filtre kahve"}
    meta.update(kw)
    govde = "Evde filtre kahve demlemek sakin bir moladır.\n\n## Oran\nBir fincan demle.\n\n## Öğütme\nTaze öğüt.\n\n## Sıcaklık\nSabırla bekle.\n\n" + "Bugün kahve demle. " * 30
    return checker.kontrol_et(yaz(tmp_path, "blog.md", meta, govde))


def test_blog_gecerli(tmp_path):
    assert not alanlar(blog(tmp_path), "hata")


def test_baslikta_anahtar_kelime_yoksa_hata(tmp_path):
    assert "anahtar_kelime" in alanlar(blog(tmp_path, baslik="Kahve Rehberi"), "hata")


def test_anahtar_kelime_alani_zorunlu(tmp_path):
    assert "anahtar_kelime" in alanlar(blog(tmp_path, anahtar_kelime=""), "hata")


def test_meta_uzunluk_uyarisi(tmp_path):
    assert any("Meta açıklama" in b.mesaj for b in blog(tmp_path, meta="evde filtre kahve").bulgular)


# ---------- telif ----------
@pytest.mark.parametrize("metin", ["Van Gogh tarzında bir fincan çiz", "Starbucks gibi demle", "Pixar gibi çiz"])
def test_stil_taklidi_ve_marka_adi_reddedilir(tmp_path, metin):
    s = checker.kontrol_et(yaz(tmp_path, "a.md", {"kanal": "instagram"}, metin))
    assert "telif_kontrolu" in alanlar(s, "hata")


def test_rtf_isteminde_stil_taklidi_yakalanir(tmp_path):
    s = checker.kontrol_et(yaz(tmp_path, "a.md", {"kanal": "instagram", "rtf_istemi": "Ghibli tarzında bir görsel"}, "Kahve demle."))
    assert "telif_kontrolu" in alanlar(s, "hata")


def test_varlik_kaydi_eksik_alan_hata(tmp_path):
    p = tmp_path / "assets.json"
    p.write_text(json.dumps([{"dosya": "a.png", "kaynak": "x", "lisans": "y", "uretim_yontemi": "z"}]), encoding="utf-8")
    assert checker.varlik_kontrol(p)[0].durum == "RED"


# ---------- kaynak doğrulama ----------
@pytest.mark.parametrize("metin", ["Araştırmalar kahvenin iyi olduğunu gösteriyor.", "Satışlar %40 arttı.", "Bu kahve sağlıklı ve bağışıklığı güçlendirir.", "Kahve zayıflatır."])
def test_kaynaksiz_iddia_reddedilir(tmp_path, metin):
    s = checker.kontrol_et(yaz(tmp_path, "a.md", {"kanal": "instagram"}, metin + " Fincan demle."))
    assert "kaynak_dogrulama" in alanlar(s, "hata")


def test_kaynak_etiketi_iddiayi_gecirir(tmp_path):
    s = checker.kontrol_et(yaz(tmp_path, "a.md", {"kanal": "instagram"}, "Satışlar %40 arttı [kaynak: iç rapor 2026]. Fincan demle."))
    assert "kaynak_dogrulama" not in alanlar(s, "hata")


def test_teknik_deger_onay_gerektirir(tmp_path):
    s = checker.kontrol_et(yaz(tmp_path, "a.md", {"kanal": "instagram"}, "Su 94 °C olsun. Fincan demle."))
    assert s.durum == "ONAY_GEREKLİ"


# ---------- gerçek içerik ----------
def test_depodaki_icerikte_hata_yok():
    sonuc = checker.tum_icerigi_kontrol(ROOT / "content")
    assert sonuc and not [s.dosya for s in sonuc if s.durum == "RED"]


def test_markdown_rapor_tum_dosyalari_listeler():
    md = checker.markdown_rapor(checker.tum_icerigi_kontrol(ROOT / "content"))
    assert "blog.md" in md and "video_tanitim.mp4" in md


# ---------- takvim ----------
def test_depodaki_takvim_gecerli():
    assert calendar_tool.dogrula(calendar_tool.yukle()) == []


def test_takvim_hatalari():
    t = calendar_tool.yukle()
    assert calendar_tool.dogrula(t[:5])
    kotu = [dict(x) for x in t]
    kotu[0]["gun"] = "Salı"
    assert any("günüdür" in h for h in calendar_tool.dogrula(kotu))
    kotu = [dict(x) for x in t]
    kotu[1]["saat"] = "25:99"
    assert any("saat" in h for h in calendar_tool.dogrula(kotu))
    kotu = [dict(x) for x in t]
    kotu[2]["sutun"] = "Rastgele"
    assert any("bilinmeyen" in h for h in calendar_tool.dogrula(kotu))
    kotu = [dict(x) for x in t]
    del kotu[3]["gerekce"]
    assert any("eksik" in h for h in calendar_tool.dogrula(kotu))


def test_takvim_excel_yazilir(tmp_path):
    import openpyxl
    calendar_tool.excel_yaz(calendar_tool.yukle(), tmp_path / "t.xlsx")
    ws = openpyxl.load_workbook(tmp_path / "t.xlsx").active
    assert ws.max_row == 8 and ws["A1"].value == "Gün"


# ---------- otomasyon ----------
def test_pipeline_onaysiz_kuyruga_almaz(tmp_path):
    k = automation.pipeline_calistir(ROOT / "content", tmp_path, onaylar={})
    assert not list((tmp_path / "queue").glob("*.json"))
    assert (tmp_path / "notifications" / "blog.txt").exists()
    assert all(x["karar"] == "ONAY_GEREKLİ" for x in k)


def test_pipeline_insan_onayi_ile_kuyruga_alir(tmp_path):
    onay = {"02_x.md": {"onaylayan": "Test Kişi", "tarih": "2026-11-10", "kapsam": ["kaynak_dogrulama"]}}
    k = automation.pipeline_calistir(ROOT / "content", tmp_path, onaylar=onay)
    q = json.loads((tmp_path / "queue" / "02_x.json").read_text(encoding="utf-8"))
    assert q["kanal"] == "x" and q["zaman"] == "2026-11-21 11:00"
    assert [x for x in k if x["dosya"] == "02_x.md"][0]["onaylayan"] == "Test Kişi"


def test_onay_kapsami_yetersizse_gecmez(tmp_path):
    onay = {"02_x.md": {"onaylayan": "T", "tarih": "2026-11-10", "kapsam": ["ton_tutarliligi"]}}
    automation.pipeline_calistir(ROOT / "content", tmp_path, onaylar=onay)
    assert not (tmp_path / "queue" / "02_x.json").exists()


def test_reddedilen_icerik_rejected_klasorune_gider(tmp_path):
    icerik = tmp_path / "icerik"
    icerik.mkdir()
    yaz(icerik, "kotu.md", {"kanal": "instagram", "planlanan": "2026-11-17 12:00"}, "Dünyanın en iyi kahvesi! Mucize!")
    k = automation.pipeline_calistir(icerik, tmp_path / "out", onaylar={})
    assert k[0]["karar"] == "RED" and (tmp_path / "out" / "rejected" / "kotu.txt").exists()


def test_cuma_tetikleyicisi():
    assert automation.cuma_09_mu(dt.datetime(2026, 11, 20, 9, 0))
    assert not automation.cuma_09_mu(dt.datetime(2026, 11, 20, 10, 0))
    assert not automation.cuma_09_mu(dt.datetime(2026, 11, 19, 9, 0))


# ---------- rapor ----------
def test_rapor_simule_isaretli(tmp_path):
    veri = ROOT / "data" / "performans_simule.csv"
    o = report.ozet(report.oku(veri))
    assert o["simule"] is True and o["toplam_goruntulenme"] > 0 and 0 < o["genel_oran"] < 1
    assert "SİMÜLE VERİ" in report.markdown(o)
    md = automation.haftalik_rapor(veri, tmp_path)
    assert md.exists() and (md.parent / "haftalik_rapor.png").exists()


def test_etkilesim_orani_sifira_bolmez():
    assert report.etkilesim_orani({"goruntulenme": 0, "begeni": 1, "yorum": 0, "paylasim": 0}) == 0.0


def test_negatif_goruntulenme_reddedilir(tmp_path):
    p = tmp_path / "v.csv"
    p.write_text("tarih,kanal,icerik,goruntulenme,begeni,yorum,paylasim,simule\n2026-11-16,x,a,-5,1,1,1,true\n", encoding="utf-8")
    with pytest.raises(ValueError):
        report.oku(p)
