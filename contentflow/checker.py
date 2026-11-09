"""AI çıktı kontrol katmanı: ton tutarlılığı, anahtar kelime, telif ve kaynak doğrulama.

Bulgular üç seviyedendir:
  hata  -> yayına alınamaz, düzeltilmeli
  uyarı -> insan onayı gerekir (ör. kaynakla doğrulanmamış teknik değer)
  bilgi -> not
"""
from __future__ import annotations

import json
import pathlib
import re
from dataclasses import dataclass, field

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALANLAR = ("ton_tutarliligi", "anahtar_kelime", "telif_kontrolu", "kaynak_dogrulama")


@dataclass
class Bulgu:
    alan: str
    seviye: str  # hata | uyarı | bilgi
    mesaj: str


@dataclass
class Sonuc:
    dosya: str
    kanal: str
    bulgular: list[Bulgu] = field(default_factory=list)

    @property
    def durum(self) -> str:
        if any(b.seviye == "hata" for b in self.bulgular):
            return "RED"
        if any(b.seviye == "uyarı" for b in self.bulgular):
            return "ONAY_GEREKLİ"
        return "GEÇTİ"

    def alan_durumu(self, alan: str) -> str:
        bs = [b for b in self.bulgular if b.alan == alan]
        return "hata" if any(b.seviye == "hata" for b in bs) else "uyarı" if any(b.seviye == "uyarı" for b in bs) else "tamam"


def marka_yukle(yol: pathlib.Path | None = None) -> dict:
    return json.loads((yol or ROOT / "brand" / "brand.json").read_text(encoding="utf-8"))


def icerik_oku(yol: pathlib.Path) -> tuple[dict, str]:
    """Basit front matter ayrıştırıcı: '---' arasındaki 'anahtar: değer' satırları."""
    metin = yol.read_text(encoding="utf-8")
    meta: dict = {}
    if metin.startswith("---"):
        _, fm, govde = metin.split("---", 2)
        for satir in fm.strip().splitlines():
            if ":" in satir:
                k, v = satir.split(":", 1)
                meta[k.strip()] = v.strip()
        return meta, govde.strip()
    return meta, metin.strip()


def _kelimeler(metin: str) -> list[str]:
    return re.findall(r"[\wçğıöşüÇĞİÖŞÜ]+", metin.lower().replace("İ", "i").replace("I", "ı"))


def _cumleler(metin: str) -> list[str]:
    govde = re.sub(r"^#+\s.*$", "", metin, flags=re.M)
    return [c.strip() for c in re.split(r"[.!?\n]+", govde) if len(c.strip().split()) >= 2]


def _icerir(metin: str, kalip: str) -> bool:
    return kalip.lower() in metin.lower()


def ton_kontrol(meta: dict, govde: str, marka: dict) -> list[Bulgu]:
    ses, b = marka["ses"], []
    temiz = govde
    for izin in ses["izinli_ifadeler"]:
        temiz = re.sub(re.escape(izin), "", temiz, flags=re.I)
    for k in ses["kacinilan_sozcukler"]:
        if re.search(rf"\b{re.escape(k)}", temiz, flags=re.I):
            b.append(Bulgu("ton_tutarliligi", "hata", f"Marka sesinde kaçınılan ifade: '{k}'"))
    if govde.count("!") > ses["max_unlem"]:
        b.append(Bulgu("ton_tutarliligi", "uyarı", f"Fazla ünlem ({govde.count('!')} > {ses['max_unlem']}); marka sesi sakin olmalı"))
    cs = _cumleler(govde)
    if cs:
        ort = sum(len(c.split()) for c in cs) / len(cs)
        if ort > ses["max_ortalama_cumle_kelime"]:
            b.append(Bulgu("ton_tutarliligi", "uyarı", f"Ortalama cümle uzunluğu {ort:.1f} kelime (sınır {ses['max_ortalama_cumle_kelime']})"))
    beklenen = ses["hitap_istisnalari"].get(meta.get("kanal", ""), ses["hitap"])
    kelimeler = set(_kelimeler(govde))
    siz_var = bool(kelimeler & {"siz", "sizi", "sizin", "size", "sizce"}) or "duymak isteriz" in govde.lower()
    sen_var = bool(kelimeler & {"sen", "seni", "senin", "sana", "sence", "dene", "demle", "dök", "bekle", "öğüt", "oku"})
    if beklenen == "sen" and siz_var:
        b.append(Bulgu("ton_tutarliligi", "uyarı", "Bu kanalda 'sen' hitabı bekleniyor, 'siz' ifadeleri var"))
    if beklenen == "siz" and sen_var and not siz_var:
        b.append(Bulgu("ton_tutarliligi", "uyarı", "Bu kanalda 'siz' hitabı bekleniyor"))
    if not any(_icerir(govde, s) for s in ses["tercih_edilen_sozcukler"]):
        b.append(Bulgu("ton_tutarliligi", "uyarı", "Marka sözlüğünden hiçbir sözcük geçmiyor"))
    if not b:
        b.append(Bulgu("ton_tutarliligi", "bilgi", "Ton uyumlu"))
    return b


def anahtar_kontrol(meta: dict, govde: str, marka: dict) -> list[Bulgu]:
    if meta.get("tur") != "blog":
        return [Bulgu("anahtar_kelime", "bilgi", "Blog dışı içerikte zorunlu değil")]
    kw, b = meta.get("anahtar_kelime", "").lower(), []
    if not kw:
        return [Bulgu("anahtar_kelime", "hata", "Blogda 'anahtar_kelime' alanı yok")]
    baslik = meta.get("baslik", "")
    if kw not in baslik.lower():
        b.append(Bulgu("anahtar_kelime", "hata", "Anahtar kelime başlıkta yok"))
    if kw not in meta.get("meta", "").lower():
        b.append(Bulgu("anahtar_kelime", "uyarı", "Anahtar kelime meta açıklamasında yok"))
    uzunluk = len(meta.get("meta", ""))
    if not 50 <= uzunluk <= 160:
        b.append(Bulgu("anahtar_kelime", "uyarı", f"Meta açıklama {uzunluk} karakter (öneri 50–160)"))
    ilk = next((p for p in govde.split("\n\n") if not p.startswith("#")), "")
    if kw not in ilk.lower():
        b.append(Bulgu("anahtar_kelime", "uyarı", "Anahtar kelime ilk paragrafta yok"))
    n_kw = govde.lower().count(kw)
    yogunluk = n_kw * len(kw.split()) / max(1, len(_kelimeler(govde))) * 100
    if not 0.4 <= yogunluk <= 3.0:
        b.append(Bulgu("anahtar_kelime", "uyarı", f"Anahtar kelime yoğunluğu %{yogunluk:.2f} (öneri %0,4–3)"))
    if len(re.findall(r"^##\s", govde, flags=re.M)) < 3:
        b.append(Bulgu("anahtar_kelime", "uyarı", "En az 3 ara başlık (H2) önerilir"))
    if not b:
        b.append(Bulgu("anahtar_kelime", "bilgi", f"'{kw}' başlıkta, metada, ilk paragrafta; yoğunluk %{yogunluk:.2f}"))
    return b


def telif_kontrol(meta: dict, govde: str, marka: dict) -> list[Bulgu]:
    t, b = marka["telif"], []
    for k in t["stil_taklidi_kaliplari"]:
        if _icerir(govde, k) or _icerir(meta.get("rtf_istemi", ""), k):
            b.append(Bulgu("telif_kontrolu", "hata", f"İsim/stil taklidi kalıbı: '{k}'"))
    for ad in t["yasakli_isimler"]:
        if re.search(rf"\b{re.escape(ad)}\b", govde + " " + meta.get("rtf_istemi", ""), flags=re.I):
            b.append(Bulgu("telif_kontrolu", "hata", f"Üçüncü taraf marka/sanatçı adı: '{ad}'"))
    if re.search(r"©|all rights reserved|unsplash|shutterstock|getty", govde, flags=re.I):
        b.append(Bulgu("telif_kontrolu", "uyarı", "Üçüncü taraf kaynak/telif ibaresi var, lisansı doğrulayın"))
    if not b:
        b.append(Bulgu("telif_kontrolu", "bilgi", "Taklit veya üçüncü taraf adı bulunmadı"))
    return b


def dogrulama_kontrol(meta: dict, govde: str, marka: dict) -> list[Bulgu]:
    d, b = marka["dogrulama"], []
    kaynakli = "[kaynak:" in govde.lower()
    for k in d["kaynak_gerektiren_kaliplar"]:
        if _icerir(govde, k) and not kaynakli:
            b.append(Bulgu("kaynak_dogrulama", "hata", f"Kaynak gerektiren iddia kalıbı '{k}' ve [kaynak: ...] etiketi yok"))
    if re.search(r"%\s?\d+|\d+\s?%", govde) and not kaynakli:
        b.append(Bulgu("kaynak_dogrulama", "hata", "Yüzde/istatistik ifadesi var, kaynak etiketi yok"))
    for k in d["saglik_iddiasi_kaliplari"]:
        if re.search(rf"\b{re.escape(k)}", govde, flags=re.I):
            b.append(Bulgu("kaynak_dogrulama", "hata", f"Sağlık iddiası kalıbı: '{k}'"))
    teknik = sorted({m.group(0) for p in d["teknik_deger_kaliplari"] for m in re.finditer(p, govde, flags=re.I)})
    if teknik and not kaynakli:
        b.append(Bulgu("kaynak_dogrulama", "uyarı", "Teknik değerler kaynakla doğrulanmadı: " + ", ".join(teknik[:8])))
    if not b:
        b.append(Bulgu("kaynak_dogrulama", "bilgi", "Doğrulama gerektiren iddia bulunmadı"))
    return b


def kanal_limiti(meta: dict, govde: str, marka: dict) -> list[Bulgu]:
    lim = marka["kanal_limitleri"].get(meta.get("kanal", ""))
    if lim and len(govde) > lim:
        return [Bulgu("ton_tutarliligi", "hata", f"{meta['kanal']} karakter sınırı aşıldı: {len(govde)} > {lim}")]
    return []


def kontrol_et(yol: pathlib.Path, marka: dict | None = None) -> Sonuc:
    marka = marka or marka_yukle()
    meta, govde = icerik_oku(pathlib.Path(yol))
    s = Sonuc(str(yol.name if hasattr(yol, "name") else yol), meta.get("kanal", "?"))
    for f in (ton_kontrol, anahtar_kontrol, telif_kontrol, dogrulama_kontrol, kanal_limiti):
        s.bulgular += f(meta, govde, marka)
    return s


def varlik_kontrol(assets_yolu: pathlib.Path, marka: dict | None = None) -> list[Sonuc]:
    """Görsel/video/ses varlıklarının kaynak–lisans–yapay zeka bildirimi alanlarını doğrular."""
    marka = marka or marka_yukle()
    out = []
    for a in json.loads(pathlib.Path(assets_yolu).read_text(encoding="utf-8")):
        s = Sonuc(a.get("dosya", "?"), "varlık")
        for alan in marka["telif"]["gerekli_varlik_alanlari"]:
            if not a.get(alan):
                s.bulgular.append(Bulgu("telif_kontrolu", "hata", f"Varlık kaydında '{alan}' eksik"))
        if "doğrulanmalı" in a.get("lisans", "").lower():
            s.bulgular.append(Bulgu("telif_kontrolu", "uyarı", "Lisans/ticari kullanım koşulu doğrulanmalı"))
        if not s.bulgular:
            s.bulgular.append(Bulgu("telif_kontrolu", "bilgi", "Kaynak, lisans ve YZ bildirimi tamam"))
        out.append(s)
    return out


def tum_icerigi_kontrol(icerik_klasoru: pathlib.Path, marka: dict | None = None) -> list[Sonuc]:
    klasor = pathlib.Path(icerik_klasoru)
    marka = marka or marka_yukle()
    sonuclar = [kontrol_et(p, marka) for p in sorted(klasor.rglob("*.md"))]
    if (klasor / "assets.json").exists():
        sonuclar += varlik_kontrol(klasor / "assets.json", marka)
    return sonuclar


def markdown_rapor(sonuclar: list[Sonuc]) -> str:
    sat = ["# İçerik Kontrol Raporu", "", "| İçerik | Kanal | " + " | ".join(ALANLAR) + " | Karar |", "|" + "---|" * (3 + len(ALANLAR))]
    for s in sonuclar:
        sat.append(f"| {s.dosya} | {s.kanal} | " + " | ".join(s.alan_durumu(a) for a in ALANLAR) + f" | **{s.durum}** |")
    sat += ["", "## Ayrıntılar"]
    for s in sonuclar:
        sat.append(f"\n### {s.dosya} — {s.durum}")
        sat += [f"- [{b.seviye}] ({b.alan}) {b.mesaj}" for b in s.bulgular if b.seviye != "bilgi" or s.durum == "GEÇTİ"]
    return "\n".join(sat) + "\n"
