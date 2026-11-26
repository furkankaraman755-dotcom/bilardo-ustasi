# Blackball Arena — Görev Haritası

Bu harita, oyunu geliştirmek için **Claude'un kendi görüşüyle** hazırladığı adım adım görev listesidir.
`YOL_HARITASI.md` büyük resmi (fazları) anlatır; bu defter ise **her oturumda yapılacak somut görevleri** tutar.

Hazırlanma: 25 Kasım 2026 · Başlangıç: **surum-72**

---

## Nasıl kullanılır
- **Sırayla gidilir.** Bir görev, "bağımlı" olduğu görevler bitmeden başlamaz.
- **Bir oturum = bir görev** (küçükse iki görev). Kota bitse bile yarım iş kalmaz.
- **Her görev şöyle biter:** test → sürüm (`surum-N`) → bu defterde ✅ → `PROJE_NOTLARI.md` güncellenir.
- **Yeni bir hata çıkarsa** "H" görevi olarak *Bilinen hatalar* listesine eklenir ve sıradaki görevden **önce** yapılır.
- **Boyut:** **K** = küçük (1 oturum) · **O** = orta (2–3 oturum) · **B** = büyük (4+ oturum)
- **Durum:** ⬜ başlamadı · 🟡 sürüyor · ✅ bitti · ⏸ beklemede

### Claude'un sıralama görüşü
Furkan 25 Kasım'da "önce yeni görseller" demişti. Benim görüşüm farklı: **önce hatalar ve temel**, sonra sunucu ve online, **görsel entegrasyonu en sonda (Aşama 9).**

Sebebi: görsel eklemek kolay ve her zaman yapılabilir. Ama temel sağlam olmadan eklenen her şey ileride yeniden elden geçmek zorunda kalır.

Önerim: Furkan görselleri şimdiden hazırlar (P-2); görseller hazır beklesin, Aşama 9'da tek seferde eklensin. Son karar Furkan'ın; isterse bu sırayı değiştiririz.

---

## Genel bakış

| Aşama | Konu | Görev sayısı | Durum |
|---|---|---|---|
| H | Bilinen hatalar | 9 | 🟡 (H-01–05, 08, 09 ✅; 07 Furkan'ın telefonda denemesini bekliyor, 06 sunucuyla) |
| 0 | Güvenlik ağı (kayıt, hata raporu) | 4 | ✅ |
| 1 | Kod ve test temeli | 10 | 🟡 (1-01, 1-02, 1-03 ✅) |
| 2 | Oyun kuralları ve fizik doğruluğu | 4 | ⬜ |
| 3 | Firebase: hesap ve bulut kayıt | 6 | ⬜ |
| 4 | Sunucuda ekonomi | 8 | ⬜ |
| 5 | Online 1'e 1 | 8 | ⬜ |
| 6 | Gelir | 4 | ⬜ |
| 7 | Yayın hazırlığı | 7 | ⬜ |
| 8 | Kapalı test ve çıkış | 6 | ⬜ |
| 9 | Büyüme ve içerik | 8 | ⬜ |
| K | Kalite ve profesyonellik (8 Ball Pool çıtası) | denetimden sonra belli olacak | ⏸ Furkan "başla" diyecek |
| P | Furkan'ın paralel görevleri | 8 | ⬜ |

Kabaca toplam: **60–75 oturum.** Düzenli çalışmayla çıkışa 3–4 ay.

---

## AŞAMA H — Bilinen hatalar ve riskler (kod incelemesinden)

**H-01 · Kayıt bozulursa her şey silinir** · K · ✅
- Sorun: Kayıt okunamazsa oyun sessizce sıfırdan başlıyor ve eski kaydın üstüne yazıyor.
- Yapılacak: Kayıt iki ayrı yuvada tutulur. Doğrulanır, bozuksa yedekten dönülür.
- Bitti: Bozuk kayıt testi → oyun yedekten açılıyor, hiçbir şey kaybolmuyor.
- ✅ surum-74: iki yuva (ana + bir adım geride yedek), doğrulama, bozuk ham veri `_bozuk` altında saklanır, "Kayıt kurtarıldı" notu.

**H-02 · Telefon hafızası dolarsa kayıt sessizce başarısız oluyor** · K · ✅
- Sorun: Kaydetme hatası yutuluyor.
- Yapılacak: Kaydetme hatası yakalanır, eski/gereksiz veri temizlenir, gerekirse oyuncuya uyarı gösterilir.
- ✅ surum-74: kota hatasında gereksizler silinir, listeler kısaltılır, tekrar denenir; olmazsa oyuncuya bir kez uyarı. NaN gibi bozuk değerler onarılıp kayda devam edilir.

**H-03 · Listelerin üst sınırı tutarsız** · K · ✅
- Sorun: Gelen kutusu, lig geçmişi ve maç kimlikleri bazı yerlerde sınırsız büyüyor.
- Yapılacak: Hepsine tek bir üst sınır kuralı.
- ✅ surum-74: `BBA_LIM` tek yerde; `bbaTrim()` her kayıttan önce uygulanır (gelen kutusu 20 + alınmamış ödüller ≤100, lig geçmişi 24, maç kimlikleri 80, ödenen dönemler 40, hata kaydı 50, iz 60).

**H-04 · Siyah ekran / dev ekranın kesin sebebi bilinmiyor** · O · ✅
- Yapılacak:
  - Açılış adımlarının süresini ve sırasını kaydeden bir "açılış izi" eklenir.
  - Cihaz bilgisi (model, Android, WebView sürümü, bellek) kaydedilir.
  - Bir sonraki olayda sebep kesin görülür.
- Bağımlı: 0-02
- ✅ surum-74: açılış izi (bu ve önceki açılış), 3. ve 10. saniyede ekran durumu, cihaz bilgisi raporda. Sebep bir sonraki olayda rapordan görülecek.

**H-05 · Test modu açık** · K · ✅
- Sorun: `TEST_UNLOCK=true` ve 10B test parası açık.
- Yapılacak: Şimdilik dokunulmaz (test için gerekli). 1-03 ile tek bayrağa bağlanır ve yayında kapanır.
- ✅ surum-75: test modu tek bayrağa (`BBA_DEV`) bağlandı; yayın APK'sında test parası, kilit açmalar ve 5 dokunuş kısayolu yok.

**H-06 · Telefon saatiyle oynanabilen ödüller** · — · ⏸
- Sorun: 46 yerde telefon saati kullanılıyor; saat ileri alınarak günlük ödül, çark vb. alınabilir.
- Yapılacak: Kalıcı çözüm sunucu saati (Aşama 4).

**H-07 · Cihazda hiç denenmemiş özellikler** · K · ⬜
- Konu: Android geri tuşu, kutu açılış videoları (otomatik oynatma), yeni paket adıyla kurulum.
- Yapılacak: Furkan'ın telefonunda kontrol listesiyle denenir (P-1). Sorun çıkarsa düzeltilir.

**H-08 · Liderlik ekranı bellek tutuyor** · K · ✅
- Sorun: Liderlik ekranından çıkınca yaklaşık 4 MB çizim alanı boşaltılmıyor.
- Yapılacak: Ekrandan çıkınca bu alanlar boşaltılır.
- ✅ surum-74: liderlikten çıkınca efekt çizim alanı 1 px'e iniyor.

**H-09 · Hata avı (surum-73)** · O · ✅
- Furkan'ın isteğiyle kod baştan tarandı, 22 hata düzeltildi (liste: `PROJE_NOTLARI.md` → surum-73). Bir denetçi alt ajan her düzeltmeyi ayrıca test edip onayladı.
- H-03'e katkı: gelen kutusu artık alınmamış ödülleri silmiyor (son 20 mesaj + ödüllüler, en fazla 100).
- Test betikleri şimdilik oturum çalışma alanında. Depoya taşınması 1-01 (testler depoya) görevinde yapılacak.

---

## AŞAMA 0 — Güvenlik ağı
Amaç: Oyuncu verisini korumak; hataları uzaktan görebilmek.

**0-01 · Çift yuvalı, doğrulamalı kayıt** · K · ✅
- = H-01 + H-02.
- Bitti: Bozuk kayıt, dolu hafıza ve yarım yazma testleri geçiyor.
- ✅ = H-01 + H-02. Testler `tests/test_kayit.py`.

**0-02 · Hata raporu ekranı** · K · ✅
- Ayarlar → Hakkında → "Hata raporunu kopyala/paylaş".
- Rapor: son 50 hata, açılış izi, cihaz bilgisi, sürüm.
- Furkan bundan sonra fotoğraf yerine tek dokunuşla metin gönderir.
- ✅ surum-74: Ayarlar → Hakkında → 📋 kopyala / 📤 paylaş. Sürüm numarasını CI yazar (`BBA_SURUM`).

**0-03 · Kayıt yedeği** · K · ✅
- Mevcut yedek kodu özelliği kontrol edilir; tek dokunuşla dosyaya yedekleme ve geri yükleme eklenir.
- Bulut kayda kadar geçici güvence.
- ✅ surum-74: Ayarlar → Güvenlik → 💾 Kaydet (İndirilenler/BlackballArena), 📂 Dosyadan yükle, 📤 Paylaş. Telefon köprüsü `BbaNative` (MainActivity). Cihazda denenmesi gerekiyor (H-07).

**0-04 · Cihaz test kontrol listesi** · K · ✅
- `docs/CIHAZ_TEST_LISTESI.md`: her sürümde telefonda 5 dakikada denenecek 15 madde.
- Örnek maddeler: açılış, menü, maç, geri tuşu, mağaza, kutu, lig, ayarlar.
- ✅ `docs/CIHAZ_TEST_LISTESI.md` hazır.

---

## AŞAMA 1 — Kod ve test temeli
Amaç: Online sistemi taşıyacak, kırılmayan ve test edilebilir bir kod. **Görünüş değişmez.**

**1-01 · Testleri depoya taşı** · O · ✅
- Bendeki ~25 Playwright testi depoya `tests/` klasörüne girer.
- GitHub'da her derlemede çalışır. Test kırmızıysa APK yayınlanmaz.
- Bitti: GitHub'da test raporu yeşil.
- ✅ surum-74: `tests/` altında 32 test; GitHub'da `test` işi, kırmızıysa `build` çalışmaz.

**1-02 · Duman testi** · K · ✅
- Bütün ekranlar tek tek açılır, konsolda hata olmaması kontrol edilir.
- Ekran görüntüleri kaydedilip bir önceki sürümle karşılaştırılır (görünüş bozuldu mu?).
- Bağımlı: 1-01
- ✅ surum-75: `tests/test_gorunus.py` 23 ekranı açar (hata olmamalı) ve önceki commit ile aynı ortamda karşılaştırır. Gürültü 0 piksel, eşik 25 piksel (bir rakam değişikliği bile yakalanır). Bilerek görünüş değiştiren commit mesajına `[görünüş]` yazılır. Fark resimleri CI'da "test-sonuclari" içinde.

**1-03 · Tek test modu bayrağı (DEV_MODE)** · K · ✅
- Test parası, kilit açmalar ve kısayollar tek bayrağa bağlanır.
- Derleme iki çıktı verir: **test APK** (açık) ve **yayın AAB** (kapalı).
- Bağımlı: 1-01
- ✅ surum-75: `window.BBA_DEV`. CI iki APK verir: `BilardoUstasi.apk` (test modu açık) ve `BlackballArena-yayin.apk` (kapalı, ayrı kayıt). AAB ve kalıcı imza 7-01'de.

**1-04 · Metinleri tek yerde topla** · O · ⬜
- Bütün Türkçe yazılar tek bir dil dosyasına taşınır.
- İngilizce ve başka diller sonradan bu dosyayla kolayca eklenir.

**1-05 · Kodu bölme 1: CSS** · O · ⬜
- 7 stil bloğu `src/css/` altına ayrılır. Derlemede birleştirilir.
- Bitti: Görsel karşılaştırma testi farksız.
- Bağımlı: 1-02

**1-06 · Kodu bölme 2: JavaScript modülleri** · B · ⬜
- Modüller: `fizik`, `kurallar`, `cizim`, `ekranlar/*`, `ekonomi`, `lig`, `ses`, `kayit`.
- Fizik ve kurallar sayfaya dokunmayan **saf kod** olur; sunucuda da çalışabilir.
- Bağımlı: 1-05

**1-07 · Ekran olay sistemi** · O · ⬜
- `show()` fonksiyonunun 11 kat sarmalanmış zinciri yerine "ekran açıldı/kapandı" olayları kurulur.
- Bütün sarmalayıcılar bu olaylara taşınır.
- Bağımlı: 1-06

**1-08 · Fizik determinizmi** · O · ⬜
- Fizik zaten sabit adımlı (1/60 sn). Fizik içindeki rastgelelik (64 kullanımdan fiziğe ait olanlar) tohumlu rastgeleye çevrilir.
- Test: Aynı 100 vuruş, hem sayfada hem Node'da birebir aynı sonucu vermeli.
- Bağımlı: 1-06

**1-09 · Temizlik** · O · ⬜
- Silinecekler: ölü kod (eski menü sürümleri, kaldırılan masa stilleri, eski haftalık lig), kullanılmayan CSS, gereksiz `!important` (şu an 1.087 tane).
- Bitti: Dosya küçüldü, testler yeşil, görünüş aynı.
- Bağımlı: 1-07

**1-10 · Bütçe kontrolleri** · K · ⬜
- CI'da otomatik sınırlar:
  - APK < 60 MB
  - index < 1 MB
  - menü ve maç ekranında çizim belleği < 30 MB
  - `a/` klasöründe kullanılmayan dosya yok
- Bağımlı: 1-01

---

## AŞAMA 2 — Oyun kuralları ve fizik doğruluğu
Amaç: Online'da iki oyuncu "kural yanlış" demesin. Kurallar bir kere ve doğru yazılsın.

**2-01 · 8 top kural tablosu** · O · ⬜
- Bütün durumlar yazılı tabloya dökülür:
  - açılış
  - grup seçimi
  - faul tipleri (beyaz top cebe, yanlış top önce, banta değmeme, ıskalama)
  - top yerleştirme
  - 8'i erken sokma
  - süre aşımı
- Her satır için otomatik test yazılır.
- Bağımlı: 1-06

**2-02 · Oda kuralları testleri** · K · ⬜
- Klasik, "Tüm Toplar Cep Seç" ve "8 Bant" kuralları test edilir.

**2-03 · Fizik gerçeklik kontrolü** · K · ⬜
- Kontrol edilecekler: cep ağızları, bant sekmesi, falso sonuçları.
- Referans vuruşların sonuç kayıtları tutulur; fiziğe dokunulduğunda fark görülür.

**2-04 · Bot zekâsı** · O · ⬜
- Botlar online'da yedek rakip olacak.
- Zorluk seviyeleri, insan gibi düşünme süresi, kontrollü hata payı, adil oyun.

---

## AŞAMA 3 — Firebase: hesap ve bulut kayıt
Amaç: Her oyuncunun kalıcı hesabı olsun.

**3-01 · Firebase projeleri** · K · ⬜
- İki proje önerilir: **test** ve **canlı**. Testler canlı oyuncuları etkilemesin.
- Furkan açar (P-4), Claude bağlar.

**3-02 · Giriş: Google + misafir** · O · ⬜
- Misafir sonradan Google'a bağlanabilir.
- Mevcut giriş ekranı görseli korunur.

**3-03 · Kalıcı 6 haneli ID** · K · ⬜
- Sunucu verir, çakışmaz.

**3-04 · Bulut kayıt** · O · ⬜
- Telefondaki kayıt ilk girişte buluta taşınır.
- İki cihazda aynı hesap açıksa çakışma kuralı uygulanır.

**3-05 · Güvenlik kuralları ve emülatör testleri** · O · ⬜
- Kurallar CI'da otomatik test edilir.

**3-06 · Hesap silme** · K · ⬜
- Google Play şartı: oyun içinden ve web'den hesap silinebilmeli.

---

## AŞAMA 4 — Sunucuda ekonomi
Amaç: Para, ödül ve puanı sunucu belirlesin. Hile ve saat oyunu biter.

**4-01 · Ekonomi tasarım belgesi** · O · ⬜
- Kaynak/harcama tablosu, başlangıç parası, ödül miktarları, kutu olasılıkları, enflasyon kontrolü.
- Furkan onaylar.

**4-02 · Sunucu fonksiyonları iskeleti** · K · ⬜
- Cloud Functions ve CI ile otomatik dağıtım.

**4-03 · Maç ekonomisi** · O · ⬜
- `startMatch` / `finishMatch`: kimlikli ve tekrarlanmaz. Bugünkü `feeGuard` mantığı sunucuya taşınır.

**4-04 · Ödüller** · O · ⬜
- Kutu, sandık, günlük hazine, çark, kartlar, altın atış ve görevler sunucudan.
- Saat sunucu saati olur (H-06 kapanır).

**4-05 · Satın alma ve envanter** · K · ⬜
- Istaka, masa, ıstaka seviye yükseltme.

**4-06 · Lig sunucuda** · O · ⬜
- 21 günlük dönem, zamanlanmış kapanış ve ödül.

**4-07 · İstemci bağlantısı** · O · ⬜
- Oyun bütün para işlemlerini sunucuya sorar.
- İnternet yoksa: antrenman oynanır, ücretli maç oynanmaz.

**4-08 · Hile testleri** · K · ⬜
- Kayıt değiştirme, saat değiştirme ve aynı isteği iki kez gönderme başarısız olmalı.

---

## AŞAMA 5 — Online 1'e 1
Amaç: Gerçek rakiple adil, kopmayan maç. Önce sade çalışsın, sonra güzelleşsin.

**5-01 · Eşleşme sırası** · O · ⬜
- Aynı oda ve ücrette bekleyenler eşleşir.
- Mevcut sinematik eşleşme ekranına bağlanır.

**5-02 · Maç odası** · O · ⬜
- Realtime Database. Sıra ve süre sunucu saatine göre işler.

**5-03 · Vuruş senkronu** · B · ⬜
- Vuruş verisi gönderilir, rakipte oynatılır.
- Her vuruştan sonra son top konumları eşitlenir.
- Bağımlı: 1-08

**5-04 · Sunucu hakemliği** · B · ⬜
- Fizik ve kural modülleri sunucuda çalışır. Kazananı sunucu belirler, şüpheli vuruşu reddeder.
- Bağımlı: 2-01, 1-08

**5-05 · Kopma ve geri bağlanma** · O · ⬜
- 30 sn içinde dönülebilir; dönülmezse hükmen yenilgi.

**5-06 · Bot yedeği** · K · ⬜
- 15 sn'de rakip bulunamazsa bot gelir.
- Bağımlı: 2-04

**5-07 · Sosyal parçalar online** · O · ⬜
- Sohbet, emoji ve hediye gerçek rakibe gider; isim ve sohbet filtresi uygulanır.

**5-08 · Gerçek dünya testi** · O · ⬜
- Yavaş internet simülasyonu.
- İki telefonla 20 maç: sonuçlar iki tarafta aynı, ödül bir kez.

---

## AŞAMA 6 — Gelir

**6-01 · Google Play ödeme** · O · ⬜
- Nakit paketleri. Sunucu satın almayı Google'a sorarak doğrular, iadeleri işler.

**6-02 · Ödüllü reklam (AdMob)** · O · ⬜
- "İzle, çip kazan." Onay penceresi (KVKK/GDPR).

**6-03 · Kutu olasılıkları ekranı** · K · ⬜
- Google kuralı.

**6-04 · TL fiyat tablosu** · K · ⬜
- Remote Config ile APK çıkarmadan değiştirilebilir. Furkan karar verir.

---

## AŞAMA 7 — Yayın hazırlığı

**7-01 · AAB ve kalıcı imza** · K · ⬜
- Play App Signing. Anahtarın iki ayrı yedeği alınır.

**7-02 · Takip araçları** · O · ⬜
- Crashlytics (oyun içi JS hataları dahil), Analytics (maç, satın alma, ekran olayları), Remote Config.

**7-03 · Gizlilik politikası ve kullanım şartları** · K · ⬜
- GitHub Pages'te ücretsiz sayfa, KVKK uyumlu.

**7-04 · Play Console formları** · K · ⬜
- Veri Güvenliği, yaş derecelendirmesi, reklam beyanı, hedef kitle.

**7-05 · Mağaza sayfası** · O · ⬜
- Türkçe ve İngilizce metin, ekran görüntüleri, öne çıkan görsel, kısa video.

**7-06 · Ucuz telefon test turu** · K · ⬜
- En az 1 eski/düşük bellekli telefonda tam tur denenir.

**7-07 · Yayın sürümü kontrolü** · K · ⬜
- DEV_MODE kapalı. Test parası yok. Bütün testler yeşil.

---

## AŞAMA 8 — Kapalı test ve çıkış

**8-01 · Kapalı test başlangıcı** · K · ⬜
- 12–20 kişi (P-6), 14 gün kesintisiz.

**8-02 · Günlük hata takibi, haftalık sürüm** · O · ⬜

**8-03 · Ölçüm ve karar noktası** · K · ⬜
- Ölçülecekler: D1/D7 geri gelme oranı, oyuncu başına maç sayısı, bırakılan ekran.
- D1 kabaca %30'un altındaysa önce oyun döngüsü düzeltilir.

**8-04 · Üretim başvurusu ve kademeli yayın** · K · ⬜
- %5 → %20 → %50 → %100.

**8-05 · Yönetim paneli** · B · ⬜
- Oyuncu ara, bakiye gör ve düzelt, banla, etkinlik ve fiyat ayarla.

**8-06 · Destek akışı** · K · ⬜
- E-posta, oyun içinden şikâyet, sık sorulan sorular.

---

## AŞAMA 9 — Büyüme ve içerik

**9-01 · Eğitim maçı** · O · ⬜
- İlk 2 dakika yeni oyuncuya oyunu öğretir.

**9-02 · Görsel paketi** · O · ⬜
- 17 ülke masası, yeni ejderha ıstakaları, kutu açılış penceresi.
- Furkan'ın P-2'de hazırladığı görseller tek seferde eklenir.

**9-03 · Sesler ve müzik** · O · ⬜
- Boyut bütçesi 60–100 MB.

**9-04 · İngilizce** · K · ⬜
- 1-04 sayesinde kolay. Sonra Arapça ve Hintçe.

**9-05 · Arkadaş sistemi** · B · ⬜
- Arkadaş listesi, kodla özel oda, davet ödülü.

**9-06 · Bildirimler** · K · ⬜
- "Günlük ödülün hazır", "arkadaşın seni davet etti".

**9-07 · Online turnuva ve 9 top** · B · ⬜

**9-08 · Kulüpler ve sezonluk etkinlikler** · B · ⬜

---

## AŞAMA K — Kalite ve profesyonellik (Furkan'ın kararı, 26 Kasım)
Furkan'ın tespiti: ✅ işareti sadece "çalışıyor ve test edildi" demek, "profesyonel" demek değil. Oyunun eksiksiz ve profesyonel görünüp hissettirmesi ayrı bir çıta.
Karar: K aşaması eklenecek. Tahminle değil, ölçerek yapılacak. **K görevleri en sona bırakılmaz, teknik görevlerin arasına yerleştirilir.**

**K-00 · Profesyonellik denetimi** · O · ⏸ (Furkan "başla" deyince ilk iş bu)
- Oyun 8 Ball Pool ile ekran ekran ve özellik özellik karşılaştırılır. Kanıt olarak ekran görüntüleri kullanılır.
- Bakılacak başlıklar:
  - Oynanış hissi: nişan, güç, falso, ses, vuruş anı.
  - Ekranların tutarlılığı: hangileri Furkan'ın görsellerinden, hangileri hâlâ kodla çizilmiş eski ekran.
  - Canlılık: geçişler, düğme tepkisi, kutlama, müzik.
  - İlk 5 dakika: yeni oyuncu ne görüyor, eğitim var mı.
  - Ucuz telefonda akıcılık.
  - Ekonomi dengesi.
  - Mağaza vitrini: ikon, Play Store sayfası, tanıtım.
- Her madde puanlanır: 🔴 amatör · 🟡 idare eder · 🟢 profesyonel.
- Çıktı: ekran görüntülü eksikler listesi (`docs/KALITE_DENETIMI.md`). Eksikler önem sırasıyla K-01, K-02… görevleri olarak bu bölüme yazılır ve sıraya yerleştirilir.
- K görevlerinin bitme şartı: "8 Ball Pool'un yanına koyunca utandırmıyor". **Son onay Furkan'ın.**
- Denetçi alt ajan bu denetimde de bağımsız göz olarak kullanılır.

---

## AŞAMA P — Furkan'ın paralel görevleri
Claude kod yazarken Furkan bunları hazırlayabilir. Böylece hiçbir aşama beklemez.

**P-1 · Cihaz kontrol listesi** · ⬜ · Her yeni sürümde 0-04'teki listeyle 5 dakikalık deneme. Sorun olursa 0-02'deki raporu gönder.

**P-2 · Görselleri şimdiden hazırla** · ⬜
- **17 ülke masası:**
  - 2D, tam üstten görünüm
  - 16:9 oranında
  - üzerinde yazı ve filigran olmasın
  - cepler önceki masalardaki gibi
- **Ejderha ıstakaları:**
  - yatay
  - kabza solda, uç sağda
  - düz siyah ya da şeffaf arka plan
  - üzerinde yazı olmasın
- Hazır olanlar bir klasörde birikebilir.

**P-3 · İsim kontrolü** · ⬜ · TÜRKPATENT ve WIPO'da "Blackball Arena" araması; 2–3 yedek isim.

**P-4 · Firebase** · ⬜
- İki proje: test ve canlı.
- Android uygulaması (`com.blackballarena.game`) ve `google-services.json`.
- Blaze planı ve bütçe uyarısı.
- Zamanı: Aşama 3 başında.

**P-5 · Google Play geliştirici hesabı** · ⬜
- 25 $.
- Kimlik doğrulaması günler sürebilir, **erken açılması iyi olur.**

**P-6 · Test kişileri listesi** · ⬜ · 12–20 kişi. Aşama 5 sırasında hazırlanmaya başlanır.

**P-7 · Destek e-postası** · ⬜ · Gizlilik politikasında ve mağazada kullanılacak.

**P-8 · Mağaza görselleri** · ⬜ · Öne çıkan görsel (1024×500) ve tanıtım görselleri. Aşama 7 öncesi.

---

**G-01 · Maç ekranı: pot çipi yeni görselle** · K · ⏸ (Furkan "bekle, başlama" dedi, 26.11.2026 21:10)
- Furkan'ın 2 fotoğrafı: `docs/bekleyen_gorseller/pot_cip_500M.png` (altın çerçeveli çip yığını, altta "500M", taç süsü) ve `docs/bekleyen_gorseller/oyun_ekrani_pot_yeri.jpg` (maç ekranı; üst ortada iki oyuncu arasındaki pot kutusu).
- İstenen: maç ekranında üst ortadaki eski çip yığınının yerine 1. fotoğraftaki çipler gelecek.
- Altındaki miktar sabit "500M" olmayacak: o maçın bahsine (potuna) göre değişecek. Örnek: İstanbul 250M giriş → 500M; Portekiz 250 → 500.
- Yapılışı: görsel parçalanır, "500M" yazısı silinip canlı yazı konur (Furkan'ın kuralı). Görsel `a/` klasörüne. Pot kutusunun yeri ve boyu bozulmaz; diğer hiçbir ayar değişmez. 9 Top, Turnuva ve ücretsiz modlarda ne görüneceği uygulamada kontrol edilir.
- Bitti: bütün odalarda doğru miktar, görünüş testi `[görünüş]`, telefonda 780×360 ve 2400×1080 kontrol.

## Sıradaki görev — NEREDE KALDIK (26.11.2026 07:36)
- **Durum:** Furkan "bekle, başlama" dedi. Şu an hiçbir iş yapılmıyor.
- **Furkan "başla / devam" deyince ilk iş: K-00 Profesyonellik denetimi** (yukarıda, AŞAMA K). Sonuçlarına göre K görevleri haritaya yerleştirilir.
- **Ondan sonra kaldığımız teknik sıra:** 1-10 (bütçe kontrolleri) → 1-04 (metinleri tek yerde topla) → 1-05 (CSS'i ayır). Son biten: 1-03 / surum-75.
- **Furkan'ın vereceği kararlar** (denetçinin surum-75 notları):
  1. 13 masa yayında da herkese bedava. Satılık mı olsun?
  2. Test APK'sı ile yayın APK'sı aynı uygulama: yan yana kurulamaz, biri diğerinin üstüne kurulur. Sorun mu?
  3. Yayında menüdeki çip sayacına dokununca mağazanın "Çip ve Nakit" sayfası açılsın mı?
- **Furkan'dan beklenen (H-07 / P-1):** surum-75'i telefona kurup `CIHAZ_TEST_LISTESI.md`'yi denemek.
- **Yeni not (26.11.2026 21:10):** Furkan pot çipi görselini gönderdi → **G-01** (yukarıda). "Bekle, başlama" dedi; "başla" deyince yapılacak.
- Denetçi alt ajan beklemede (kapatılmadı); devam edilince kaldığı yerden çalışır.
- **Sunucu kararı (Furkan, 26.11.2026):** Oyun sunucusu **Hetzner**'de olacak. Firebase'in de kullanılıp kullanılmayacağı sonra konuşulacak. Aşama 3–5 bu karara göre yeniden düzenlenecek.

## Değişiklik günlüğü
- 26.11.2026 21:10 — G-01 eklendi (maç ekranı pot çipi, miktar bahse göre). Beklemede.
- 26.11.2026 — surum-76: Furkan'ın 12 yeni görseli araya alındı (giriş + pencereler + 6 dil, mavi ana menü, 4 sekmeli mağaza, 3B Masalar ekranı). 9-02 Görsel paketinin bir kısmı öne çekildi. Teknik sıra değişmedi (sırada K-00 / 1-10).
- 26.11.2026 — AŞAMA K (Kalite ve profesyonellik) eklendi; K-00 Profesyonellik denetimi Furkan'ın "başla"sını bekliyor. Furkan "bekle" dedi; nerede kalındığı "Sıradaki görev"e yazıldı.
- 26.11.2026 — surum-75: 1-02, 1-03, H-05 ✅. Ayarlar → Güvenlik'te etiket taşması düzeltildi, telefonun yazı boyutu artık ekranları bozmuyor (setTextZoom 100).
- 26.11.2026 — surum-74: H-01, H-02, H-03, H-04, H-08, 0-01, 0-02, 0-03, 0-04, 1-01 ✅ (denetçi alt ajan her birini ayrıca test edip onayladı).
- 25.11.2026 — H-09 eklendi ve bitti: surum-73 hata avı (22 düzeltme).
- 25.11.2026 — Görev haritası oluşturuldu (Claude'un görüşü). Kod incelemesinden 8 bilinen hata eklendi.
