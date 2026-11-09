# ContentFlow — Kıvam Kahve

Yapay Zeka ile İçerik Üretimi Eğitimi final projesi. Kurgusal bir kahve markası (**Kıvam Kahve**) için marka stratejisi, 7 günlük içerik takvimi ve uçtan uca bir içerik seti üretildi; üzerine zorunlu kapsamın ötesinde **çalışan bir kontrol, otomasyon ve raporlama aracı** eklendi.

## Teslim edilenler (`deliverables/`)
| Teslim | Dosya |
|---|---|
| Marka Stratejisi Dokümanı (1 sayfa) | `1_Marka_Stratejisi_Dokumani.docx` |
| İçerik Takvimi (7 gün, Excel) | `2_Icerik_Takvimi.xlsx` |
| Örnek İçerik Seti | `icerik_seti/`: blog, 3 gönderi, 3 görsel, 18,6 sn video (Türkçe altyazılı), seslendirme |
| Kontrol listesi + AI kullanım raporu + prompt kütüphanesi | `4_Kontrol_ve_AI_Kullanim_Raporu.docx` |
| Tek sunum (Canva'ya aktarılabilir) | `ContentFlow_Kivam_Kahve_Teslim_Sunumu.pptx` |

## Zorunlu kapsamın ötesi (isteğe bağlı pratikler)
```bash
pip install -r requirements.txt
python -m contentflow kontrol --rapor out/kontrol.md   # 1) AI çıktı kontrol katmanı
python -m contentflow takvim                          # takvimi doğrula + Excel üret
python -m contentflow pipeline                        # 2) tetikleyici→eylem akışı (yerel simülasyon)
python -m contentflow rapor                           # 3) performans raporu (SİMÜLE veri)
pytest                                                # 37 test
```
- **Kontrol katmanı** (`contentflow/checker.py`): `ton_tutarliligi`, `anahtar_kelime`, `telif_kontrolu`, `kaynak_dogrulama`. Kural tabanlıdır: yasaklı sözcükler, ünlem sayısı, hitap (sen/siz, kanala göre), blog SEO (başlık, meta, ilk paragraf, yoğunluk, H2), stil taklidi/marka adı, kaynaksız istatistik ve sağlık iddiası, varlık kayıtlarında kaynak–lisans–YZ bildirimi. Seviyeler: **hata** (red), **uyarı** (insan onayı gerekir), bilgi.
- **Otomasyon** (`contentflow/automation.py`, `automation/scenarios.json`): Make/Zapier mantığında akış tasarımı ve yerel simülasyonu. GEÇTİ → kuyruk; ONAY_GEREKLİ → bildirim; RED → reddedilenler. Uyarılar yalnızca adı, tarihi ve kapsamı olan bir insan onayıyla (`brand/onaylar.json`) geçer. Gerçek Make/Zapier/Buffer/Slack hesabına **bağlı değildir**.
- **Performans raporu** (`contentflow/report.py`): etkileşim oranı, kanal özeti, grafik. **Veri SİMÜLEDİR** (`data/performans_simule.csv`, `simule=true`); gerçek yayın sonucu değildir ve raporlarda uyarı olarak basılır.

## Dürüstlük notları
- **Görseller ve video üretken yapay zeka ile değil**, Python (Pillow, ffmpeg) ile kodla çizildi (`tools/generate_media.py`). Eğitmen üretken görsel/video aracı bekliyorsa prompt kütüphanesindeki istemlerle yeniden üretilmelidir.
- **Seslendirme** Microsoft Edge'in Türkçe yapay sesidir (edge-tts); ticari kullanım koşulları doğrulanmalıdır.
- **Kontrol aracı** demleme değerlerini (1:16, 90–96 °C, süreler) kaynaksız teknik değer olarak `ONAY_GEREKLİ` işaretler. Bu değerler proje sahibi tarafından 9 Kasım 2026'da onaylandı; onay `brand/onaylar.json` içinde ad, tarih ve kapsamla kayıtlıdır. Ses dosyasının lisans uyarısı onaylanmamıştır ve açıktır.
- Rakip bilgileri genel konumlandırmadır; güncel kaynakla doğrulanmalıdır. Marka kurgusaldır.


## Klasörler
`brand/` marka kuralları · `content/` yayın metinleri (front matter'lı Markdown) · `calendar/` takvim JSON · `contentflow/` araç kodu · `automation/` akış tasarımı · `tools/` medya ve belge üreticileri · `tests/`
