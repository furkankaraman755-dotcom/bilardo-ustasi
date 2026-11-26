# Blackball Arena — Yol Haritası Defteri

Bu defter adım adım ne yapacağımızı tutar. Her adım bitince durumu güncellenir.
Proje geçmişi ve teknik bilgiler: `docs/PROJE_NOTLARI.md`
Görev görev ayrıntılı liste (Claude'un önerdiği sıra): `docs/GOREV_HARITASI.md`

Oluşturulma: 25 Kasım 2026 · Başlangıç noktası: **surum-72**

**Durum işaretleri:** ⬜ başlamadı · 🟡 sürüyor · ✅ bitti · ⏸ beklemede

---

## Ana kurallar
1. **Sırayla gidilir.** Bir faz bitmeden sonrakine geçilmez. Online sistem sağlam temel ister.
2. **Kozmetik dondurma (Claude'un önerisi):** Furkan önce yeni görselleri istedi (Faz G: ülke masaları, ejderha ıstakaları). Faz G bitince Faz 8'e kadar yeni masa, ıstaka, efekt ve tasarım eklenmemesi, sadece hata düzeltilmesi önerilir. Son karar Furkan'ın; gelen görseller saklanır, Faz 9'da eklenir.
3. **Her adım şöyle biter:** test → sürüm → Furkan telefonda dener → bu defter güncellenir.
4. **Görünüşü bozma kuralı** her fazda geçerli.
5. Her fazın sonunda bir **"bitti sayılır"** şartı var. Şart sağlanmadan faz kapanmaz.

---

## Genel durum tablosu

| Faz | Konu | Tahmini süre* | Durum |
|---|---|---|---|
| 0 | Kararlar ve hazırlık | 1–3 gün | 🟡 (çoğu verildi) |
| G | Görsel paketi (Furkan'ın seçimi) | görsellerin gelmesine bağlı | 🟡 sıradaki |
| 1 | Temeli sağlamlaştırma | 1–2 hafta | ⬜ |
| 2 | Firebase: giriş ve bulut kayıt | ~1 hafta | ⬜ |
| 3 | Sunucuda ekonomi ve güvenlik | 1–2 hafta | ⬜ |
| 4 | Online 1'e 1 | 3–5 hafta | ⬜ |
| 5 | Gelir: ödeme ve reklam | ~1 hafta | ⬜ |
| 6 | Play Store hazırlığı | ~1 hafta | ⬜ |
| 7 | Kapalı test (zorunlu 14 gün) | 2–3 hafta | ⬜ |
| 8 | Türkiye'de yumuşak çıkış | 2–4 hafta | ⬜ |
| 9 | Büyüme | sürekli | ⬜ |

\* Süreler düzenli çalışma varsayımıyla kabaca verildi. Toplamda gerçekçi hedef: **çıkışa 3–4 ay.**

---

## FAZ 0 — Kararlar ve hazırlık 🟡
Amaç: Sonradan geri dönülemeyecek kararları baştan vermek.

- [ ] **0.1 Kozmetik dondurma.** Furkan önce Faz G'yi seçti. Faz G sonrası için karar bekleniyor.
- [x] **0.2 Kalıcı paket adı.** ✅ `com.blackballarena.game` (surum-72'de uygulandı). Eski uygulama silinmeli; yeni APK ayrı uygulama olarak kurulur.
- [ ] **0.3 İsim kontrolü.** TÜRKPATENT ve WIPO'da "Blackball Arena" aranır. Play Store'da "Blackball" adlı oyun olduğu için yedek 2–3 isim de hazır tutulur.
- [ ] **0.4 İlk pazar.** Öneri: önce Türkiye, sonra İngilizce ile global.
- [x] **0.5 Küçük kararlar:**
  - ✅ 1'e 1'de **ülke masası kalır**; seçilen masa 1'e 1'e uygulanmaz.
  - ✅ Özel Teklif %30 indirimli: Destansı Kutu **11** (1 tane) / **31** (3 tane), surum-72. Günde bir kez sınırı istenirse eklenir.
  - ⬜ Yeni oyuncunun başlangıç parası (Faz 3.4'te).
- [ ] **0.6 Hesaplar** (Furkan, ücretsiz):
  - Firebase/Google hesabı hazır
  - Destek için bir e-posta (ör. blackballarena.destek@gmail.com)

**Bitti sayılır:** 0.1–0.4 kararları bu deftere yazıldı.

---

## FAZ G — Görsel paketi (Furkan'ın seçimi, 25 Kasım) 🟡 sıradaki
Furkan, Firebase'den önce yeni görsellerin yapılmasını seçti.
- [ ] **G.1 Ülke masaları.**
  - Furkan 17 ülke için masa fotoğrafı gönderir.
  - Her biri ülke odasına bağlanır; cepler fizik ceplerine hizalanır, yazı ve filigran temizlenir.
  - 1'e 1'de ülke masası kullanılmaya devam eder.
- [ ] **G.2 Yeni ejderha ıstakaları.**
  - Furkan kendi görsel aracıyla üretir.
  - Claude arka planı temizler; ıstakalar standarda (Ejder ölçüsü, kabza solda, uç sağda) otomatik oturur.
- [ ] **G.3** Faz G sonunda bellek ve boyut kontrolü (APK hedefi < 60–100 MB), tüm testler.

**Bitti sayılır:** Gönderilen görsellerin hepsi oyunda; testler geçiyor. Sonra Faz 1'e geçilir.

---

## FAZ 1 — Temeli sağlamlaştırma ⬜
Amaç: Online sistemi taşıyacak sağlam ve test edilebilir bir kod. **Oyunun görünüşü hiç değişmez.**

- [x] **1.1 Testleri projeye taşı.** ✅ surum-74 (32 test, `tests/`)
  - Şu an bendeki ~25 Playwright testi depoya `tests/` klasörüne girer.
  - GitHub'da her derlemede otomatik çalışır.
  - Test kırılırsa APK yayınlanmaz.
- [ ] **1.2 Kodu modüllere böl.**
  - Tek dosya `index.html` (5.300 satır) → `src/` altında parçalar:
    - `fizik.js` (sunucuda da çalışacak)
    - `cizim.js`
    - `ekranlar/…`
    - `ekonomi.js`
    - `lig.js`
    - `ayarlar.js`
  - Derlemede tek dosyada birleştirilir. Oyun aynı kalır.
- [ ] **1.3 Sarmalayıcı zincirini temizle.**
  - Ekran açma fonksiyonu 11 kat sarmalanmış → tek bir "ekran açıldı/kapandı" olay sistemi.
  - CSS'teki 1.087 `!important` azaltılır.
- [ ] **1.4 Fiziği deterministik yap.**
  - Sabit zaman adımı.
  - Fizik içinde rastgelelik yok (gerekirse tohumlu rastgele).
  - **Test:** Aynı vuruş 100 kez → hep aynı sonuç.
  - Online maçın temel şartı budur.
- [x] **1.5 Test modunu tek yere topla.** ✅ surum-75 (`BBA_DEV`; yayın APK'sı ayrıca derleniyor)
  - `TEST_UNLOCK`, test parası (10B), test kısayolları tek bir `DEV_MODE` ayarına bağlanır.
  - Yayın sürümünde otomatik kapanır.
- [ ] **1.6 Gerçek cihaz testi.** Furkan ve yakınlarından en az 1 eski/ucuz telefonda deneme yapılır. Hata kaydı ekranı kontrol edilir.

**Bitti sayılır:**
- Tüm testler GitHub'da yeşil.
- Fizik deterministik testi geçiyor.
- Oyun telefonda öncekiyle aynı görünüyor ve çalışıyor.

---

## FAZ 2 — Firebase: giriş ve bulut kayıt ⬜
Amaç: Her oyuncunun kalıcı bir hesabı olsun; telefon değişse de hiçbir şey kaybolmasın.

**Furkan yapar** (Claude adım adım anlatır):
- [ ] **2.1** console.firebase.google.com → proje "Blackball Arena".
- [ ] **2.2** Android uygulaması ekle (Faz 0'daki paket adı) → `google-services.json` dosyasını Claude'a gönder.
- [ ] **2.3** Authentication → **Google** ve **Anonim** girişi aç.
- [ ] **2.4** Firestore ve Realtime Database oluştur (bölge: europe-west).
- [ ] **2.5** Blaze planı ve **bütçe uyarısı** (ör. aylık 10 $).
- [ ] **2.6** Hizmet hesabı anahtarı → GitHub → Settings → Secrets → `FIREBASE_SERVICE_ACCOUNT`.

**Claude yapar:**
- [ ] **2.7** Paket adı değişikliği ve Firebase eklentileri. Test sürümleri yeniden kurulacak, eski test kayıtları gider.
- [ ] **2.8** Giriş ekranı: "Google ile giriş" + "Misafir". Misafir hesap sonradan Google'a bağlanabilir.
- [ ] **2.9** Kalıcı **6 haneli oyuncu ID'si.** Sunucu verir, çakışmaz.
- [ ] **2.10** Bulut kayıt: bakiye, ıstakalar, masalar, seviye, lig → Firestore `players/{uid}`.
- [ ] **2.11** Facebook girişi (isteğe bağlı, sonra). Meta geliştirici uygulaması ve onayı gerekir.

**Bitti sayılır:** Oyunu sil → yeniden kur → aynı Google hesabıyla gir → her şey geri geliyor.

---

## FAZ 3 — Sunucuda ekonomi ve güvenlik ⬜
Amaç: Para, ödül ve puanı telefon değil sunucu belirlesin. Hile yapılamasın.

- [ ] **3.1 Güvenlik kuralları.** Telefon bakiye, puan ve envanter alanlarına yazamaz, sadece sunucu fonksiyonları yazar.
- [ ] **3.2 Sunucu fonksiyonları (Cloud Functions).** Her işlem kimlikli olur, iki kez işlenmez.
  - `startMatch`: ücreti düşer, maç kaydı açar
  - `finishMatch`: ödülü bir kez verir, lig puanını ekler
  - `openBox`: kutu ödülünü sunucu seçer
  - `buyItem`: ıstaka ve masa alımı
  - `claimReward`: günlük ödül, çark, kartlar, görevler
  - `seasonClose`: 21 günlük lig dönemi, zamanlanmış
- [ ] **3.3 Saat.** Bütün zamanlar sunucu saatinden alınır; telefonun saatini değiştirmek işe yaramaz.
- [ ] **3.4 Ekonomi tasarımı** (Furkan + Claude birlikte):
  - Başlangıç parası
  - Kazanç/harcama dengesi tablosu
  - Kutu içerikleri ve olasılıkları
  - Özel Teklif fiyatı
  - Lig eşiklerinin gözden geçirilmesi
  - Test parasının kalkması
- [ ] **3.5 Ekonomi testleri.** Kayıt dosyasını değiştirmek, saati değiştirmek ve aynı isteği iki kez göndermek bakiyeyi bozmamalı.

**Bitti sayılır:** Bütün para hareketleri sunucuda; hile denemeleri testte başarısız oluyor.

---

## FAZ 4 — Online 1'e 1 (en büyük iş) ⬜
Amaç: Gerçek rakiple, adil ve kopmayan maç. **Önce sade çalışsın, sonra güzelleşsin.**

- [ ] **4.1 Eşleşme sırası.** Aynı masa ve ücrette bekleyen oyuncular eşleşir. 15 sn içinde rakip yoksa bot rakip gelir. Bot adil oynar.
- [ ] **4.2 Maç odası (Realtime Database).** Sıra, süre, vuruş verisi (açı, güç, falso, top yerleştirme).
- [ ] **4.3 Senkron.**
  - Vuruşu yapan telefon fiziği oynatır, rakip telefon da aynı vuruşu oynatır.
  - Her vuruştan sonra son top konumları eşitlenir, küçük farklar birikmez.
- [ ] **4.4 Sunucu doğrulaması.**
  - Sunucu aynı fizik kodunu (Faz 1.2'deki `fizik.js`) çalıştırır, vuruşları kontrol eder.
  - Kazananı sunucu belirler.
- [ ] **4.5 Bağlantı kopması.** 30 sn içinde maça dönülebilir. Dönülmezse hükmen yenilgi, rakip ödülü alır.
- [ ] **4.6 Mevcut özelliklerin online hâli.** Sohbet, emoji ve hediye gerçek rakibe gider. Eşleşme ekranında gerçek rakibin adı ve avatarı görünür.
- [ ] **4.7 Turnuva online** (Faz 4 sonu ya da Faz 9).

**Bitti sayılır:**
- İki telefonla en az 20 maç sorunsuz oynanıyor.
- Sonuç iki telefonda aynı.
- Ödül bir kez veriliyor.
- Bağlantı kopması doğru işleniyor.

---

## FAZ 5 — Gelir ⬜
- [ ] **5.1 Google Play ödeme sistemi.** Nakit paketleri, kutular. Her satın alma sunucuda Google'a sorularak doğrulanır.
- [ ] **5.2 TL fiyat tablosu** (Furkan karar verir).
- [ ] **5.3 Ödüllü reklam (AdMob).** "Reklam izle, çip kazan." Kullanıcı onay penceresi (KVKK/GDPR).
- [ ] **5.4 Kutu olasılıkları.** Oyunda görünür hâle gelir (Google kuralı).

**Bitti sayılır:** Test hesabıyla satın alma, iptal ve iade doğru çalışıyor. Reklam ödülü bir kez veriliyor.

---

## FAZ 6 — Play Store hazırlığı ⬜
- [ ] **6.1** Google Play geliştirici hesabı (tek seferlik 25 $). Furkan açar.
- [ ] **6.2** APK yerine **AAB** formatı ve kalıcı imza anahtarı. Anahtarın yedeği iki ayrı güvenli yerde saklanır.
- [ ] **6.3** `DEV_MODE` kapalı yayın sürümü: test parası ve test kısayolları yok.
- [ ] **6.4** Gizlilik politikası ve kullanım şartları sayfası (KVKK uyumlu, GitHub Pages'te ücretsiz).
- [ ] **6.5** Play Console formları: Veri Güvenliği, yaş derecelendirmesi, reklam beyanı, hedef kitle.
- [ ] **6.6** Mağaza sayfası: simge, öne çıkan görsel, 6–8 ekran görüntüsü, kısa video, Türkçe ve İngilizce açıklama.
- [ ] **6.7** Takip araçları: Crashlytics (çökmeler), Analytics (oyuncu davranışı), Remote Config (APK çıkarmadan fiyat ve etkinlik değişikliği).

**Bitti sayılır:** Kapalı test sürümü Play Console'a yüklendi ve onaylandı.

---

## FAZ 7 — Kapalı test (Google'ın zorunlu şartı) ⬜
- [ ] **7.1** En az **12, tercihen 20 test kişisi** (arkadaş, aile, gruplar). Furkan Faz 4 sırasında listeyi hazırlamaya başlar.
- [ ] **7.2** **14 gün kesintisiz** test. Her gün çökme raporlarına ve geri bildirime bakılır, hatalar düzeltilir.
- [ ] **7.3** Ölçülür:
  - 1. gün geri gelme oranı (D1)
  - 7. gün geri gelme oranı (D7)
  - Oyuncu başına maç sayısı
  - Oyuncuların hangi ekranda bıraktığı
- [ ] **7.4** **Karar noktası.**
  - D1 kabaca **%30'un altındaysa** önce oyun döngüsü düzeltilir: eğitim maçı, ödül dengesi, eşleşme süresi.
  - Değilse üretime başvurulur.
- [ ] **7.5** Play Console'dan üretim erişimi başvurusu.

**Bitti sayılır:** Üretim erişimi onaylandı.

---

## FAZ 8 — Türkiye'de yumuşak çıkış ⬜
- [ ] **8.1** Kademeli yayın: %5 → %20 → %50 → %100. Her basamakta çökme ve donma oranları kontrol edilir.
- [ ] **8.2** **Yönetim paneli:** oyuncu arama, bakiye görme ve düzeltme, banlama, etkinlik ve fiyat ayarı.
- [ ] **8.3** Destek: e-posta, isim ve sohbet filtresi, şikâyet etme.
- [ ] **8.4** Küçük reklam testi (ör. 50–100 $). Bir oyuncu getirmenin maliyeti ölçülür. Oyuncular kalıyorsa bütçe büyütülür.

**Bitti sayılır:** %100 yayında. Çökme oranı düşük. İlk gerçek oyuncu verileri elde.

---

## FAZ 9 — Büyüme ⬜
Kozmetik dondurma burada kalkar.
- [ ] **9.1** Eğitim maçı, İngilizce dil, kaliteli sesler ve menü müziği (boyut bütçesi 60–100 MB).
- [ ] **9.2** Arkadaş listesi, kodla özel oda, kulüpler, davet ödülü, bildirimler ("günlük ödülün hazır").
- [ ] **9.3** Online 9 top ve diğer modlar. Sezonluk etkinlikler.
- [ ] **9.4** Bekleyen görsel işler:
  - Ülke masalarının görselleri
  - Yeni ejderha ıstakaları
  - Yeni masa paketleri
  - Kutu açılış penceresi
- [ ] **9.5** Yeni diller ve ülkeler: Arapça, Hintçe vb.
- [ ] **9.6** Facebook girişi (Faz 2'de yapılmadıysa).

---

## Furkan'ın şimdiden paralel yapabilecekleri
- [ ] Faz G görselleri: 17 ülke masası, yeni ejderha ıstakaları
- [ ] İsim kontrolü (TÜRKPATENT/WIPO)
- [ ] Firebase projesini açmak (Faz 2.1–2.6)
- [ ] Kapalı test için 12–20 kişilik liste
- [ ] Mağaza sayfası için görseller: öne çıkan görsel (1024×500), tanıtım görselleri
- [ ] Gizlilik politikası için iletişim bilgisi (e-posta)
- [ ] Google Play geliştirici hesabı (25 $)

## Tahmini maliyetler
- **Google Play geliştirici hesabı:** 25 $ (tek sefer)
- **Firebase:** Başlangıçta ücretsiz kotalarla büyük ihtimalle 0–10 $/ay. Bütçe uyarısı konacak.
- **Gizlilik sayfası:** GitHub Pages ile ücretsiz.
- **Reklam testi:** İsteğe bağlı, 50–100 $ ile başlanabilir.

## Riskler ve önlemler
| Risk | Önlem |
|---|---|
| Kod temeli kırılgan | Faz 1: modüller ve otomatik testler |
| Online senkron sorunları | Deterministik fizik, her vuruştan sonra konum eşitleme, sunucu doğrulaması |
| Hile | Faz 3: her şey sunucuda; Play Integrity |
| Telefona özel hatalar (siyah ekran vb.) | Ucuz telefonda test, hata kaydı, Crashlytics |
| Google kuralları (kutular, çip bahsi) | Olasılıkları göster, doğru yaş derecesi, gerçek para karşılığı yok |
| İsim/marka çakışması | Faz 0.3 kontrolü, yedek isimler |
| Kota veya oturum kesintisi | Bu defter + `PROJE_NOTLARI.md` + testler depoda; her oturum kaldığı yerden devam eder |
| Pazarlama bütçesi yok | Önce oyuncu tutma (D1/D7) kanıtlanır, sonra küçük bütçeyle büyünür |

---

## Değişiklik günlüğü (bu defterin)
- 26.11.2026 07:36 — Furkan'ın kararı: oyun sadece çalışır değil, **eksiksiz ve profesyonel** olmalı. Görev haritasına AŞAMA K (Kalite ve profesyonellik) eklendi; ilk iş K-00 Profesyonellik denetimi (8 Ball Pool karşılaştırması). Şu an ⏸ beklemede; Furkan "başla" deyince oradan devam.
- 26.11.2026 — **surum-75**: Test modu tek bayrağa bağlandı (1.5 ✅). CI artık test APK'sı ile yayın APK'sını ayrı veriyor. Görünüş karşılaştırma testi eklendi.
- 26.11.2026 — **surum-74**: Görev haritasındaki güvenlik ağı tamamlandı: çift yuvalı kayıt, hafıza dolu koruması, liste sınırları, hata raporu + açılış izi, dosyaya yedek, cihaz test listesi, liderlik belleği. Testler depoya taşındı ve CI'da APK'dan önce çalışıyor (1.1 ✅).
- 25.11.2026 — **surum-73: hata avı, 22 düzeltme** (Furkan'ın isteği; denetçi alt ajan her düzeltmeyi ayrıca test edip onayladı). En önemlileri: pes edince çift maç sonucu, resimli avatarla açılışta betiğin yarıda kalması (fullFit/hile koruması çalışmıyordu), sıfırla/yedekten yükle çalışmıyordu, çift kutu alımı, kayıp çark/kart ödülleri, iade sonrası bedava maç, isimde HTML kodu. Liste: `PROJE_NOTLARI.md` → surum-73. Plan sırası değişmedi.
- 25.11.2026 — `GOREV_HARITASI.md` eklendi. Claude'un önerisi: önce hatalar ve temel, görsel entegrasyonu sonda. Furkan'ın "önce görseller" seçimiyle farklı; son karar Furkan'ın.
- 25.11.2026 — Defter oluşturuldu. surum-72 kararları işlendi: paket adı, 1'e 1 ülke masası, Özel Teklif 11/31. Sıradaki iş: **Faz G (görseller)**, ardından Faz 1.1.
