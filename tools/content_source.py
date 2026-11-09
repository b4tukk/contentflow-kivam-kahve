# -*- coding: utf-8 -*-
"""Kıvam Kahve içerik metinleri — tek kaynak (belge, Excel ve slayt buradan beslenir)."""

BRAND = "Kıvam Kahve"
TAGLINE = "Acele etme, tadına var."
HANDLE = "@kivamkahve"
PALETTE = [("Espresso", "#3B2A20", "Ana metin, koyu zemin"), ("Krema", "#E8D5B7", "Sıcak zemin, vurgu"),
           ("Bakır", "#C8693A", "Eylem çağrısı, sayılar"), ("Adaçayı", "#7A8B6F", "Buhar, ikincil çizgiler"), ("Krem Beyazı", "#FAF6EF", "Açık zemin")]
VALUES = ["Sabır", "Şeffaflık", "Paylaşım"]

WHY = "Evde kahve demlemek isteyip uzman jargonundan çekinen insanlara sakin, ölçülü ve yargılamayan bir rehber olmak."
WHO = "Elif, 29, şehirde yaşayan, hibrit çalışan bir grafik tasarımcı. Evde filtre kahve denemeye yeni başladı; 'doğru yöntem' tartışmalarından sıkılıyor, kısa ve uygulanabilir bilgi istiyor. Günün en keyifli anı sabah ilk fincanı."
WHAT = "Her hafta tek bir pratik demleme bilgisi, sade bir üretici hikâyesi ve küçük bir 'mola' anı."
HOW = "Sıcak, sakin, bilgili ama ukala değil. Kısa cümleler, somut ölçüler (gram, saniye), bol boşluk ve doğal renkler."

TONE_DO = ["Samimi ve sakin: 'sen' diliyle konuş", "Somut ol: gram, derece, süre ver", "Cesaretlendir: 'Dene, beğenmezsen ayarla'", "Kısa cümle, tek fikir"]
TONE_DONT = ["'En iyi', 'mucize', 'kusursuz' gibi abartılar", "Sağlık iddiası (zayıflatır, hastalığı önler vb.)", "Küçümseyen uzman dili ('yanlış yapıyorsun')", "Ünlü marka veya sanatçı adıyla stil taklidi"]
VOCAB = ["kıvam", "demle", "yavaş", "mola", "tadına var", "fincan", "sabır"]
AVOID = ["acele", "hızlı çözüm", "hack", "şok", "kaçırma"]

PILLARS = [
    ("1. Demleme Rehberi", "Evde filtre kahveyi basit ölçülerle anlatan eğitici içerik", "Elif'in temel ihtiyacı: 'Nasıl yapacağım?'"),
    ("2. Çiftlikten Fincana", "Kahvenin yolculuğu; üretici ve kavurma hikâyeleri", "Şeffaflık değeri; fincanın arkasındaki emek"),
    ("3. Mola Anları", "Yavaşlama, sohbet ve günlük ritüel; topluluk etkileşimi", "Paylaşım değeri; kahveyi duygusal bağa çevirir"),
    ("4. Küçük Denemeler", "Küçük karşılaştırmalar (oran, süre) ve topluluk anketleri", "Merak; öğrenirken eğlenme"),
]

COMPETITORS = [
    ("Starbucks Türkiye", "Global zincir; yaygın erişim, standart deneyim", "Kişisel, sakin ve eğitici dil boşluğu"),
    ("Kahve Dünyası", "Yerli zincir; Türk kahvesi ve çikolata geleneği", "Evde filtre demleme eğitimi boşluğu"),
    ("Espresso Lab", "Üçüncü dalga kahve zinciri; kahveye odaklı", "Başlangıç seviyesi için daha sade anlatım fırsatı"),
    ("Mahalle kavurmacıları", "Küçük, tutkulu, çoğu zaman jargonlu", "Jargonsuz, düzenli yayın akışı"),
    ("Online abonelik markaları", "Kapıya teslim, kişiselleştirilmiş paket", "Rehberlik + topluluk (sadece ürün değil)"),
]
COMP_NOTE = "Not: Rakip bilgileri genel bilinen konumlandırmalara dayanır, sayısal veri içermez. Yayından önce güncel kaynaklardan doğrulanmalıdır (bkz. kontrol listesi)."

# ---------------- BLOG ----------------
BLOG_TITLE = "Evde Filtre Kahve Nasıl Demlenir? 5 Adımda Dengeli Bir Fincan"
BLOG_META = "Evde filtre kahve demlemek zor değil. Kahve-su oranı, su sıcaklığı ve öğütme kıvamıyla 5 adımda dengeli bir fincan hazırlayın."
BLOG_KEYWORDS = "evde filtre kahve, filtre kahve nasıl demlenir, kahve su oranı, pour over"
BLOG = [
    ("p", "Sabah ilk fincanı sakin bir şekilde hazırlamak, günün tonunu belirler. İyi haber şu: **evde filtre kahve** demlemek için pahalı ekipman ya da barista deneyimi gerekmez. Bir demleme aparatı, bir tartı ve biraz sabır yeterli."),
    ("h", "1. Oranı baştan belirle"),
    ("p", "Başlangıç için yaygın bir oran 1:16'dır: 1 gram kahveye 16 gram su. 20 gram kahve için 320 gram su gibi. Genellikle 1:15 ile 1:17 arası denenir; daha yoğun istersen suyu azalt, daha hafif istersen artır. Mutfak tartısı bu işi çok kolaylaştırır."),
    ("h", "2. Kahveyi demlemeden hemen önce öğüt"),
    ("p", "Öğütülmüş kahve aromasını hızla kaybeder. Mümkünse çekirdeği demlemeden hemen önce, orta kalınlıkta (genellikle iri tuz kıvamına yakın) öğüt. Çok ince öğütürsen kahve acılaşır, çok kalın öğütürsen sulu ve ekşi kalır."),
    ("h", "3. Suyun sıcaklığına dikkat et"),
    ("p", "Çoğu kaynak filtre kahve için yaklaşık 90–96 °C arasını önerir. Su kaynadıktan sonra yarım ila bir dakika bekletmek genellikle işini görür. Filtre kağıdını ılık suyla önceden ıslat; hem kağıt tadını alır hem de aparatı ısıtır."),
    ("h", "4. Suyu yavaş ve daire çizerek dök"),
    ("p", "Önce kahvenin iki katı kadar suyla kahveyi ıslat ve yaklaşık 30 saniye bekle (buna 'çiçeklenme' denir). Sonra kalan suyu küçük dairelerle, birkaç aşamada dök. Toplam demleme süresi çoğunlukla 2,5–3,5 dakika arasındadır."),
    ("h", "5. Tadı oku, bir sonraki fincanı ayarla"),
    ("p", "Fincan ekşi ve sulu mu? Biraz daha ince öğüt ya da biraz daha sıcak su dene. Acı ve kuru mu? Biraz daha kalın öğüt ya da biraz daha kısa süre dene. Her seferinde yalnızca tek bir şeyi değiştir; bu sayede neyin neye yaradığını öğrenirsin."),
    ("h", "Son söz"),
    ("p", "Mükemmel fincan diye bir şey yok; senin tadına uyan fincan var. Acele etme, tadına var. Haftaya Kıvam Kahve'de çiftlikten fincana yolculuğu konuşacağız."),
]

# ---------------- SOSYAL ----------------
POSTS = [
    dict(kanal="Instagram", sutun="Demleme Rehberi", gorsel="gorsel_2_demleme_orani.png",
         rtf="ROL: Sakin, samimi bir kahve rehberi (Kıvam Kahve marka sesi). GÖREV: Evde filtre kahve yapan yeni başlayanlar için 1:16 oranını tanıtan bir Instagram gönderisi yaz. FORMAT: En fazla 70 kelime; ilk satırda kanca, 1 soru, 3 hashtag; sağlık iddiası ve abartı yok.",
         metin="Kahveni tartıyor musun? ⚖️\n\nBaşlangıç için basit bir ölçü: 1 gram kahve, 16 gram su. Yoğun mu geldi? Biraz azalt. Hafif mi? Biraz artır.\n\nBu hafta bir fincanı ölçerek demle, sonra bize tadını anlat. Sence hangi oran sana uyuyor?\n\nAcele etme, tadına var.\n\n#evdefiltrekahve #kıvamkahve #demlemerehberi"),
    dict(kanal="X (Twitter)", sutun="Küçük Denemeler", gorsel=None,
         rtf="ROL: Kıvam Kahve'nin sakin ve meraklı sesi. GÖREV: Takipçileri küçük bir demleme denemesine davet eden bir tweet yaz. FORMAT: 280 karakteri geçmesin; somut ölçü içersin; 1 soru; hashtag en fazla 1.",
         metin="Küçük deney: aynı kahve, aynı su, iki fincan.\nBirini 1:15, diğerini 1:17 oranıyla demle.\nHangisi daha dengeli geldi? Yorumlara yaz, sonuçları cumartesi birlikte konuşalım ☕\n#kıvamkahve"),
    dict(kanal="LinkedIn", sutun="Mola Anları", gorsel="gorsel_1_marka_karti.png",
         rtf="ROL: Kıvam Kahve'nin kurucu sesi, sakin ve içten. GÖREV: Çalışanlara 'yavaşlama molası' fikrini anlatan bir LinkedIn gönderisi yaz. FORMAT: 90-110 kelime; kısa paragraflar; bilimsel iddia veya istatistik yok; son cümle marka sloganı.",
         metin="Günün ortasında 5 dakika. Sadece bir fincan.\n\nUzaktan ya da ofiste çalışıyor olsanız da, ekrandan başınızı kaldırıp bir şeyi sabırla yapmak iyi geliyor: su ısıtmak, kahveyi tartmak, damlaları izlemek.\n\nKıvam Kahve'de bunu 'mola' diyoruz. Bir ritüel, bir tartı, bir sakin an.\n\nSiz günün hangi anında yavaşlıyorsunuz? Yorumlarda duymak isteriz.\n\nAcele etme, tadına var."),
]

VOICE = "Güne yavaş başla. Kıvam Kahve ile evde filtre kahve demlemek çok kolay. Bir gram kahveye on altı gram su. Suyu yavaşça dök, sabırla bekle. Kıvam Kahve. Acele etme, tadına var."

# ---------------- TAKVİM ----------------
CAL_HEAD = ["Gün", "Tarih", "Saat", "İçerik sütunu", "Format", "Kanal", "Konu", "Gerekçe (hedef kitle bağlantısı)", "Marka sesi notu", "Üretim", "Dosya", "Durum"]
CAL = [
    ["Pazartesi", "16.11.2026", "09:00", "Demleme Rehberi", "Blog yazısı", "Web sitesi blogu", "Evde filtre kahve nasıl demlenir?", "Hafta başında Elif'in temel sorusunu yanıtlar; arama trafiği (SEO) getirir.", "Somut ölçü, sakin ton", "Claude (metin)", "icerik_seti/blog_yazisi.docx", "Hazır"],
    ["Salı", "17.11.2026", "12:30", "Demleme Rehberi", "Instagram gönderisi", "Instagram", "1:16 başlangıç oranı", "Blogdaki ana bilgiyi öğle arasında kolay tüketilen görsele çevirir.", "Soru ile etkileşim", "Claude (metin) + Python (görsel)", "gorsel_2 + gönderi 1", "Hazır"],
    ["Çarşamba", "18.11.2026", "18:00", "Çiftlikten Fincana", "Hikâye görseli", "Instagram Story", "Çiftlikten fincana yolculuk", "Akşam rahat saatinde markanın şeffaflık değerini görselleştirir.", "Sade, abartısız", "Python (görsel)", "gorsel_3", "Hazır"],
    ["Perşembe", "19.11.2026", "19:00", "Demleme Rehberi", "Kısa video + seslendirme", "Instagram Reels", "Güne yavaş başla (18 sn)", "Video, haftanın en yüksek erişim potansiyeli olan format; akşam kaydırma saati.", "Sakin tempo, TTS sesi", "Python + edge-tts", "video_tanitim.mp4", "Hazır"],
    ["Cuma", "20.11.2026", "09:30", "Mola Anları", "LinkedIn gönderisi", "LinkedIn", "Günün ortasında 5 dakika", "Çalışan kitleye mola ritüelini anlatır; marka hikâyesini profesyonel kanala taşır.", "İçten, yargısız", "Claude (metin)", "gönderi 3 + gorsel_1", "Hazır"],
    ["Cumartesi", "21.11.2026", "11:00", "Küçük Denemeler", "Tweet + anket", "X (Twitter)", "1:15 mi, 1:17 mi?", "Hafta sonu zamanı olan Elif'e küçük bir deney önerir; etkileşim ölçülür.", "Merak uyandıran, kısa", "Claude (metin)", "gönderi 2", "Hazır"],
    ["Pazar", "22.11.2026", "20:00", "Mola Anları", "Topluluk sorusu", "Instagram Story", "Bu hafta en çok hangi fincan keyif verdi?", "Hafta sonu akşamı topluluk etkileşimi; yeni haftanın içerik fikirlerini toplar.", "Sıcak, samimi", "Elle + sticker", "(planlı)", "Planlı"],
]

# ---------------- KONTROL ----------------
CHK_HEAD = ["İçerik", "Marka sesi tutarlılığı", "Telif / etik", "Halüsinasyon riski", "Sonuç ve alınan aksiyon"]
CHK = [
    ["Blog yazısı", "✔ 'Sen' dili, somut ölçüler, abartı yok", "✔ Özgün metin; alıntı yok", "⚠ Oran (1:15–1:17), sıcaklık (90–96 °C), süre (2,5–3,5 dk) genel kabul gören aralıklardır; bu çalışmada kaynakla doğrulanmadı", "Yayından önce SCA/üretici kılavuzlarıyla doğrula. Metin 'genellikle/yaklaşık' ifadesiyle yumuşatıldı. İstatistik/sağlık iddiası yok."],
    ["Instagram gönderisi", "✔ Soru ile biten sakin ton", "✔ Özgün", "✔ Sadece 1:16 oranı (blogla aynı)", "Hashtag'ler gerçek bir marka adı içermiyor."],
    ["X gönderisi", "✔ Merak uyandıran, kısa", "✔ Özgün", "✔ İddia yok, deney önerisi", "280 karakter sınırı kontrol edildi."],
    ["LinkedIn gönderisi", "✔ İçten, yargısız", "✔ Özgün", "✔ Bilimsel iddia/istatistik bilinçli olarak çıkarıldı", "'Mola iyi gelir' gibi kesin sağlık iddiası yerine kişisel deneyim dili kullanıldı."],
    ["Görsel 1–3", "✔ Yalnızca marka paleti (5 renk)", "✔ Kodla çizildi; üçüncü taraf görsel/stil taklidi yok. Yazı tipleri Windows sistem fontları (Georgia, Segoe UI)", "✔ Gerçek ürün/kişi gösterilmiyor", "Ticari kullanımda font lisansı kontrol edilmeli veya açık lisanslı fonta geçilmeli."],
    ["Video", "✔ Aynı palet ve slogan", "✔ Müzik yok (telif riski yok)", "✔ Videodaki tek bilgi 1:16 oranı", "Süre 18,6 sn (15–20 sn şartı). Sosyal medyada 'yapay zeka ile üretilmiştir' notu önerilir."],
    ["Seslendirme", "✔ Sakin tempo, aynı metin", "⚠ Yapay ses (Microsoft Edge TTS, tr-TR-EmelNeural). Ticari kullanım koşulları doğrulanmalı", "✔ Metinle aynı", "Gerçek kişi sesi taklit edilmedi. Ticari yayında lisanslı TTS servisi (ör. Azure Speech) önerilir."],
    ["Rakip analizi", "—", "✔ Sadece genel konumlandırma", "⚠ Rakip tanımları genel bilgiye dayanır, kaynak gösterilmedi", "Yayın/sunum öncesi güncel kaynakla doğrula."],
]

# ---------------- AI KULLANIM RAPORU ----------------
AI_HEAD = ["Görev", "Araç", "Neden bu araç?", "Karşılaşılan sorun ve çözüm"]
AI = [
    ["Marka analizi, strateji, ses rehberi, takvim", "Claude (Claude Code)", "Uzun, yapılandırılmış Türkçe metin ve tutarlı çerçeve (Neden-Kime-Ne-Nasıl) üretimi", "Rakip bilgisi uydurma riski → yalnızca genel konumlandırma yazıldı, doğrulama notu eklendi."],
    ["Blog, 3 sosyal medya gönderisi", "Claude (RTF formülü)", "Marka sesi rehberine bağlı, kanala göre biçim kuralı verilebilmesi", "LinkedIn'de istatistik eğilimi → istem 'istatistik yok' kuralıyla sınırlandı."],
    ["3 görsel + video karesi", "Python (Pillow) ile kodla çizim", "Marka paletini birebir uygulamak ve telif riski olmaması", "İlk sürümde çizim başlık metniyle çakıştı → ölçek ve konum düzeltildi. NOT: Bunlar üretken görsel yapay zeka çıktısı değildir; istenirse aşağıdaki istemlerle Midjourney/DALL·E ile yeniden üretilebilir."],
    ["Kısa video (18,6 sn)", "Python + ffmpeg (imageio-ffmpeg)", "Tekrarlanabilir, ücretsiz, tam kontrol", "İlk seslendirme 21,7 sn çıktı (20 sn sınırı) → metin kısaltıldı, 17,1 sn oldu."],
    ["Seslendirme", "edge-tts (Microsoft Edge Türkçe nöral ses)", "Doğal Türkçe telaffuz; Windows'taki yerleşik sesler yalnızca İngilizce", "Ticari lisans belirsiz → kontrol listesine not düşüldü."],
]

PROMPTS = [
    ("Marka kimliği (Aşama 1-2)", "RTF — Rol: Kıdemli marka stratejisti. Görev: Evde filtre kahve eğitimi veren kurgusal bir Türk kahve markası için Neden-Kime-Ne-Nasıl çerçevesini, persona, ses tonu ve 4 içerik sütununu yaz. Format: Başlıklı, maddeli, 2 sayfayı geçmeyen Türkçe doküman."),
    ("Blog", "CO-STAR — Bağlam: Kıvam Kahve (sakin, bilgili, ukala olmayan). Hedef: Evde filtre kahveye yeni başlayanlar. Stil/Ton: marka sesi rehberine uygun. Çıktı: SEO için 'evde filtre kahve' anahtar kelimeli, 5 adımlı, ~450 kelimelik blog; sağlık iddiası ve istatistik yok."),
    ("Görsel (Midjourney/DALL·E için, isteğe bağlı yeniden üretim)", "Minimal flat illustration of a pour-over coffee dripper on a small carafe, warm espresso brown #3B2A20, cream #FAF6EF, copper #C8693A, sage green steam lines, lots of negative space, no text, vertical 4:5. (Sanatçı veya marka adı kullanılmaz.)"),
    ("Video (Runway vb. için, isteğe bağlı)", "15-20 second vertical video, calm slow pace, flat illustrated pour-over coffee being brewed, drops falling, soft steam, palette espresso/cream/copper, no people, no music, end card with text 'Kıvam Kahve'."),
    ("Seslendirme", "Metin: bkz. seslendirme_metni.txt. Ses: tr-TR-EmelNeural, normal hız, sakin ton."),
]
