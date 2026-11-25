# Blackball Arena — Proje Not Defteri

Yeni bir sohbette her şeyi baştan anlatmamak için tutulur.
Yeni sohbette ilk mesaj: **"docs/PROJE_NOTLARI.md dosyasını oku, oradan devam et."**

Son güncelleme: 25 Kasım 2026 · Son sürüm: **surum-71**

---

## BÖLÜM 1 — Projenin kimliği

| Konu | Bilgi |
|---|---|
| Oyunun adı | **Blackball Arena** (önce "Bilardo Ustası", kısa süre "8 Blackball Arena") |
| Tür | Mobil 8 top bilardo; online ve çok oyunculu olacak |
| Hedef | Google Play Store (milyonlarca indirme hedefleniyor) |
| Örnek alınan | 8 Ball Pool |
| Sahibi | Furkan. Sadece telefondan çalışıyor, bilgisayar yok |
| Depo | github.com/furkankaraman755-dotcom/bilardo-ustasi |
| APK indirme | `…/releases/download/surum-N/BilardoUstasi.apk` |
| Paket adı | `com.bilardoustasi.oyun` (Play Store'dan önce kalıcı ad seçilecek; öneri `com.blackballarena.game`) |
| Tasarım dili | Siyah + altın; mor vurgular; turnuva mavisi varsayılan masa |
| Para birimleri | **Çip** (siyah-altın taçlı "B" çip görseli), **Nakit** (yeşil banknot destesi), **Elmas** |

### Furkan'ın kalıcı kuralları
1. **"Bekle / başlama / not al"** → sadece not alınır. **"Başla" / "yap"** → uygulanır.
2. **Başka hiçbir şeyin ayarı bozulmaz.** Sadece istenen değişir.
3. **Ekranlar Furkan'ın görsellerine birebir yapılır:** Görsel parçalanır, yazılar silinip canlı yazı konur. Ekranlar tam ekran olur ve butonlar çalışır. Kodla çizilmiş taklit "acemice" bulundu, istenmiyor.
4. Masa görselleri toplu gelir, "yap" denince soru sormadan her biri ayrı tema olarak eklenir.
5. Gerçek kişi benzerliği ve telifli karakter (Naruto, Goku vb.) yapılmaz.
6. Yeni APK kurmadan önce eskisi silinmeli (şu an test imzası kullanılıyor).
7. Play Store öncesi: test parası (10B) ve test kilit açmaları kaldırılacak. İsim TÜRKPATENT/WIPO'da kontrol edilecek.
8. Furkan görsel üretir (kendi yapay zekâ aracıyla). Claude resim üretemez; görselleri oyuna yerleştirir, temizler ve hizalar.

---

## BÖLÜM 2 — Teknik altyapı

- **Oyun kodu:** Tek dosya `index.html` (~0,56 MB, ~5300 satır). HTML5 + JavaScript, Canvas 2D. Fizik motoru tamamen bize ait.
- **Görseller:** `a/` klasöründe ~110 WebP ve 3 MP4 (kutu efektleri), ~4,6 MB. HTML'e gömülmez, dosya yoluyla yüklenir.
- **Android:** Capacitor 8 (WebView).
  - `native/MainActivity.java`: tam ekran ve Android geri tuşu.
  - `native/res`: uygulama simgeleri.
- **Derleme (CI):** `.github/workflows/build.yml`. Her push'ta bulutta APK derlenir ve `surum-N` olarak yayınlanır.
  - Sadece not/belge değişikliğinde commit mesajına `[skip ci]` yazılır.
  - Maven 429 hatası olursa iş yeniden çalıştırılır (`gh api -X POST …/actions/runs/<id>/rerun`).
- **Boyut:** APK 9,2 MB. Tavan 60–100 MB.
- **Kayıt:** Şu an her şey telefonda (`localStorage` → `save` nesnesi). Sunucu yok.
- **Yöntem:** Yeni özellikler, eski fonksiyonları sarmalayan ve dosyanın sonuna eklenen betiklerle yapılır. Böylece eski kod bozulmaz.
- **Görsel ekranlar:** Tasarım koordinatlarıyla kurulur (`--x/--y/--w/--h`), `--k` ile ölçeklenir, `fullFit` ile tam ekrana gerilir.
- **Önemli kod parçaları:**
  - Çekirdek: `save`, `TABLES`, `ROOMS`, `ALL_CUES`, `LEAGUES`, `BOXES`, `show()`, `startGame()`, `gameOver()`, `drawTable()`, `drawCue()`, `resize()`, `loop()`
  - Para ve güvenlik:
    - `antiCheat`: maçtan kaçan kaybeder.
    - `feeGuard`: giriş ücreti iadesi.
    - `lifecycle`: 30 sn'den uzun arka planda kalırsa yeniden başlatma.
  - Kararlılık:
    - `ensureScreen`: siyah ekran koruması.
    - `selfHeal`: ekran ölçüsü düzeltme.
    - `freeGame`: bellek boşaltma.
    - `bbaLog`: hata kaydı (Ayarlar → Hakkında'da görünür).
  - Görsel:
    - `chipFly2`: çip uçuşu.
    - `imgTables`: resimli masalar.
    - `cueStdDraw`: ıstaka standardı.
    - `boxFx`: kutu videoları.
    - `ofFit`: Özel Teklif kartı.
  - Lig: `lgCredit`, `lgTick`, `renderLead`, `openLead`, `leadGoBack`
  - Geri tuşu: `bbaBack`

---

## BÖLÜM 3 — Şimdiye kadar ne yaptık (baştan sona)

### Başlangıç kararları
- Furkan önce Godot denedi, zor buldu. Kod tabanlı web oyunu yazılıp Android'e paketlenmesine karar verildi.
- Ücretli uygulama yapıcılar (Easyapp vb.) yerine GitHub + bulut derleme seçildi. Claude GitHub uygulaması depoya bağlandı.

### 19 Kasım — Temel oyun
- Oyun ve Android derleme kuruldu; APK'lar Releases sayfasına konuyor.
- **Oynanış:**
  - Yatay masa, ıstakayı çekerek güç, falso.
  - Zamana bağlı fizik, gerçekçi cepler (köşe ~2,3 top, orta ~1,7 top ağız, çene çarpışmaları).
  - 3B dönen toplar, numaralı parlak toplar, cebe süzülme, top haznesi (tepsi ve raylı).
- **Ekranlar ve sistemler:**
  - Giriş ekranı, profil/ID, seviye, ana menü.
  - 17 şehir masası, turnuva, günlük ödül.
  - İstakalar (Standart/Zafer/Sürpriz; Güç/Odak/Falso/Süre özellikleri, seviye atlatma).
  - Mağaza (kutular, ücretsiz ödüller, teklif), sandık yuvaları, lig.
  - Oyun modları: 9 top, kılavuzsuz, şanslı atış, egzersiz, atış süresi.
  - Görevler, şans çarkı, kazı kazan, başarımlar, gelen kutusu, ayarlar, avatar seçimi, maç içi emojiler.
- **Masalar:** Turnuva (kırmızı bantlı açık mavi), Saray Halısı, Mor Saray.
- **Ses:** Örnek tabanlı gerçekçi bilardo sesleri.
- **Ekran yerleşimi:** Tam ekran (çentik dahil). Oyun ekranı 8 Ball Pool düzeninde (üstte oyuncu-pot-rakip, solda güç, sağ üstte falso).
- Oyun içi menü (Devam / Pes Et / Kapat), test için 5 milyar altın.

### 20 Kasım — Fizik, ıstaka, tema
- **Masa ölçüleri:** Referans fotoğraflara göre (oyun alanı 2:1, banda gömülü cepler). Gerçek falso: durdurma, takip, geri çekme, sağ/sol.
- **Fizik 3 aşamada iyileştirildi:**
  1. Gecikmesiz nişan, ince ayar tekerleği
  2. Çok geçişli çarpışma, kesme sürtünmesi, bant enerji kaybı
  3. Gerçekçi top aydınlatması
- **Vuruş hissi:** Gerçek vuruş hareketi (ıstaka topa değince top çıkar), sıra gelince ıstakanın topa yaklaşması.
- **Eşleşme ve ilerleme:**
  - 8 Ball Pool tarzı sinematik eşleşme: rakip arama, VS ekranı, çiplerin pota akışı, İptal.
  - 1000 seviyelik XP/unvan sistemi.
  - Sohbet, hediye ve beğeni; kız/erkek, çok dilli rakipler.
- **Masalar:** Ligli ülke masaları (Underdog → Royal), her ülkeye özel çuha rengi ve deseni, "Tüm Toplar Cep Seç" kuralı.
- **İstakalar:**
  - 6 + 16 yeni gerçek anatomili ıstaka.
  - MAX ıstaka: bantlardan seken nişan izi, hassas nişan.
  - 3 MAX ejderha ıstakası (gökkuşağı enerji efekti).
  - İstakalar ekranı yeniden yapıldı (koleksiyon gücü, 6 sekme, arama ve sıralama).
- **Tema:** Önce neon tema, sonra mor-altın tema, Roboto yazı tipi, çuhaya BLACKBALL logosu. Ad "Blackball Arena" oldu.

### 21 Kasım (gece) — Furkan'ın görsellerinden ekranlar
- Giriş efekti (logo, 4,5 sn), uygulama simgesi.
- Görsel parçalanarak yapılan ekranlar:
  - Ana menü (siyah-altın), giriş ekranı, profil (tam ekran), ıstaka seçici
  - Liderlik Tablosu (10 lig: Novice, Pioneer, Nova, Rogue, Valor, Astra, Zenith, Dominion, Eclipse, Paragon)
  - Ayarlar (7 sekme, İptal/Kaydet, yedek kodu), Avatar Seç (14 resim, 9 renk)
  - Hediyeler: Efsane Sandıklar, Şans Çarkı, Gizemli Kartlar, Altın Atış, Günlük Hazine
  - Mağaza kutuları
- Ekranlar tam ekrana gerildi (`fullFit`).

### 21–22 Kasım — Sürümler 63–71
- **surum-63:**
  - Uygulama simgesi seçenek C (logo kırpılmadan).
  - Siyah ekran için ilk düzeltme.
  - 30 sn arka plan kuralı ve hile koruması (maçtan kaçan kaybeder, ücret iade edilmez).
  - Menüde Furkan'ın para çubuğu görseli, sağ üst ayar çarkı kaldırıldı.
  - Her yerde yeni çip ve banknot simgeleri, potta B çip yığını.
- **surum-64:**
  - İstaka standardı: 84 ıstakanın hepsi Ejder ölçüsünde, kabza solda, uç sağda, ortalı, tüm ekranlarda; yeni ıstakalar da otomatik uyar.
  - Kısa ıstaka isimleri (Ejder, Volkan, Fırtına, Galaksi, Zümrüt…).
  - Kalan eski simgeler değişti (ıstaka menüsü, çark).
- **surum-65:** 6 resimli masa (Pembe Saray, Zehir Neon, Buz Kristal, Kızıl Ateş, Zümrüt Saray, Gece Moru). Cepler fizik ceplerine hizalandı, Çince yazılar silindi.
- **surum-66:**
  - Siyah ekran koruması ve hata kaydı.
  - Çip toplama animasyonu baştan: çipler sayaca uçuyor, sayaç parlıyor.
  - Günün Teklifi'nde siyah-altın Destansı Kutu.
- **surum-67:** Grafik belleği düzeltmesi.
- **surum-68 (sağlamlık sürümü):**
  - Görseller dosyalara taşındı (HTML 5,4 MB → 0,5 MB, açılış 2 kat hızlı).
  - Istaka listesinde sadece görünenler çiziliyor, maçtan çıkınca bellek boşaltılıyor.
  - Giriş ücreti iadesi: maç açılamazsa, 16 sn takılırsa ya da oyun kapanırsa.
  - Oyun ekranı kendi ölçüsünü düzeltiyor.
- **surum-69:**
  - 9 yeni masa görseli: 5'i temiz sürümle yenilendi, 4 yeni (Elektrik Mavi, Kara Altın, Gümüş Saray, Lav Alevi). "AI tarafından oluşturulan içerik" yazısı silindi.
  - "8 USTA" yazılı masalar kaldırıldı.
  - Özel Teklif: Furkan'ın FIRSAT kartı (canlı fiyat ve butonlar).
- **surum-70:**
  - 21 günlük lig dönemi: net kazanç puanı, "Mevcut Ligim / Sonraki Lig", kalan süre, dönem sonu ödülü, geçmiş.
  - Geri düğmesi önceki sayfaya dönüyor. Android geri tuşu: önce pencereyi kapatır, ana menüde uygulamayı arka plana alır.
  - Sürpriz Kutuları açılış efekti Furkan'ın videosundan (sekme açılınca vitrin, satın alınca açılış).
- **surum-71:**
  - Demo masalar kaldırıldı (Royal Turnuva, Neon Gece, Klasik Yeşil, Okyanus, Bordo, Gece, Mor Lüks, Kraliyet).
  - Turnuva, Saray Halısı ve Mor Saray, "8 BLACKBALL ARENA" baskısıyla geri geldi.
  - Mağazadaki masa adı hatası düzeldi.

### Bugünkü içerik (özet)
- **Ülke masaları (1'e 1):** 17 oda. Ödül = 2 × giriş, net kazanç = giriş.
  - Portekiz 250 · İtalya 1K · Fransa 4K · Hollanda 5K · Brezilya 10K · Japonya 50K · Mısır 100K
  - İspanya 250K · Almanya 500K · İngiltere 1M · Rusya 2,5M · Kore 5M · Amerika 10M
  - Dubai 25M · Monako 50M · Las Vegas 100M · İstanbul 250M
  - 1'e 1'de ülkenin kendi masası kullanılır.
- **Turnuva:** Giriş 1000, ödül 7500, 3 tur.
- **Masalar (13):**
  - Klasik 3: Turnuva (varsayılan), Saray Halısı, Mor Saray
  - Resimli 10: Pembe Saray, Zehir Neon, Buz Kristal, Kızıl Ateş, Zümrüt Saray, Gece Moru, Elektrik Mavi, Kara Altın, Gümüş Saray, Lav Alevi
- **İstakalar:** 84.
- **Kutular (1 tane / 3 tane, nakit):** Nadir 5/14 · Destansı 16/44 · Efsanevi 33/89.
- **Lig eşikleri (21 günlük net kazanç):** Novice 0 · Pioneer 30K · Nova 150K · Rogue 300K · Valor 1M · Astra 3M · Zenith 10M · Dominion 30M · Eclipse 100M · Paragon 300M.
  - Dönem sonu ödülü: eşiğin %10'u çip + 1 elmas.
  - İlk dönem 17 Kasım 2026'da başladı.

### Yaşanan hatalar ve dersler
| Sorun | Sebep | Çözüm |
|---|---|---|
| Kodla çizilen ekranlar beğenilmedi | Görsele birebir değildi | Görseli parçalama yöntemi |
| Ekranlar tam ekran değildi | Sabit oran | `fullFit` ile germe |
| Para simgeleri taştı | Çizilen simgeler | Furkan'ın kendi para çubuğu görseli |
| İlk açılışta siyah ekran, bozuk/dev oyun ekranı | Büyük ihtimalle WebView grafik belleği doldu | Görseller dosyaya taşındı, bellek boşaltma, `ensureScreen`, `selfHeal`, hata kaydı |
| Çip kesildi, maç açılmadı | Ücret maç kurulmadan alınıyordu | `feeGuard` ile iade |
| Çipler sola uçuyordu | Gizli kapsayıcıyı hedef alıyordu | Görünen sayaca uçuş, sabit katman |
| Mağazada masa adı bozuk | Başka bir `.nm` CSS kuralı | Kural kapsamlandı |
| surum-70 notunda "Dubai 25 bin" yazıldı | Yanlış bilgi | Doğrusu 25 milyon |

> Siyah ekran ya da bozuk ekran tekrar olursa: **oyunu silmeden önce Ayarlar → Hakkında'daki "Hata kaydı"nın fotoğrafı çekilip gönderilsin.**

---

## BÖLÜM 4 — Bundan sonra ne yapacağız (adım adım)

### Hemen bekleyen küçük işler
1. **Ülke masaları:** Furkan fotoğraf gönderebilir. Ayrıca seçilen masanın 1'e 1'de de kullanılıp kullanılmayacağına karar verilecek. Seçenekler:
   - a) Seçilen masa her maçta
   - b) Ülke masası kalsın
   - c) Ayarlardan seçilsin
2. **Özel Teklif fiyatları:** Karar verilecek. Şu an normal Destansı fiyatı, günlük indirim kapalı.
3. **Yeni ejderha ıstakaları:** Furkan görselleri üretecek, Claude yerleştirecek. Standarda otomatik oturuyorlar.

### ADIM 1 — Firebase kurulumu (Furkan + Claude)
**Furkan yapar:**
1. console.firebase.google.com → yeni proje "Blackball Arena".
2. Kalıcı paket adını onayla (öneri `com.blackballarena.game`) → Android uygulaması ekle → `google-services.json` dosyasını indirip Claude'a gönder.
3. Authentication → Google, Facebook ve Anonim girişi aç. Facebook için Meta geliştirici uygulaması gerekir, Claude adım adım anlatır.
4. Firestore Database'i oluştur (bölge: europe-west).
5. Blaze planına geç ve harcama limiti koy (ör. aylık 5–10 $).
6. Proje ayarları → Hizmet hesapları → yeni özel anahtar oluştur → GitHub deposunda Settings → Secrets'a `FIREBASE_SERVICE_ACCOUNT` olarak ekle. Claude adım adım anlatır.

**Claude yapar:** Paket adı değişikliği, Firebase eklentilerinin projeye eklenmesi, CI'nin sunucu kodunu otomatik yüklemesi.

### ADIM 2 — Giriş ve bulut kayıt
- Google / Facebook / misafir girişi. Misafir hesap sonradan Google'a bağlanabilir.
- Her oyuncuya kalıcı **6 haneli ID**.
- Bakiye, ıstakalar, masalar, seviye ve lig Firestore'a kaydedilir; telefon değişse de kaybolmaz.
- Eski telefondaki kayıt ilk girişte buluta taşınır.
- **Test:** Oyunu sil, yeniden kur, aynı hesapla gir → her şey geri gelmeli.

### ADIM 3 — Sunucuda ekonomi (hile koruması)
- Bakiye alanlarına telefon yazamaz, sadece sunucu fonksiyonları yazar.
- Sunucu fonksiyonları:
  - `startMatch`: ücreti düşer, maç kaydı açar
  - `finishMatch`: ödülü bir kez yazar, lig puanını ekler
  - `openBox`: kutu ödülünü sunucu belirler
  - `claimDaily`: günlük ödül
  - `seasonClose`: zamanlanmış dönem kapanışı ve ödüller
- Zaman sunucu saatinden alınır; telefon saatini değiştirmek işe yaramaz.
- Plan ayrıntısı: `docs/lig-sunucu.md`
- **Test:** Kayıt dosyasıyla oynamak ve saat değiştirmek bakiyeyi etkilememeli.

### ADIM 4 — Online 1'e 1 (asıl büyük iş)
1. **Eşleşme sırası:** Aynı masa/ücret için bekleyen oyuncular eşleşir. 10–15 sn içinde rakip bulunamazsa bot rakip gelir.
2. **Vuruş senkronu:** Her vuruşta sadece açı, güç, falso ve top yerleşimi gönderilir (Realtime Database). İki telefon aynı fizikle aynı sonucu hesaplar.
3. **Fizik deterministik yapılacak:** Sabit zaman adımı, rastgelelik yok; her telefonda aynı sonuç çıkmalı.
4. **Sunucu doğrulaması:** Aynı fizik kodu sunucuda çalışır ve şüpheli vuruşu reddeder.
5. **Bağlantı kopması:** 30 sn içinde dönülebilir; dönülmezse maç kaybedilir.
6. **Sohbet ve emojiler:** Gerçek rakibe gider.
- **Test:** İki telefonla aynı masada oyna; sonuç ikisinde de aynı olmalı, kazanan ödülü bir kez almalı.

### ADIM 5 — Gelir
- Google Play Billing ile nakit paketleri ve kutular. Her satın alma sunucuda Google'a sorularak doğrulanır.
- AdMob ödüllü reklam ("izle, çip kazan"). Kullanıcı onayı (KVKK/GDPR, UMP).
- Kutu olasılıkları oyunda gösterilir (Google kuralı).

### ADIM 6 — Play Store hazırlığı
1. APK yerine AAB formatı, kalıcı imza anahtarı (yedeği güvenli yerde saklanacak).
2. Test parası, test kilitleri ve test kısayolları kaldırılacak.
3. Gizlilik politikası ve kullanım şartları sayfası (KVKK uyumlu).
4. Play Console: Veri Güvenliği formu, yaş derecelendirmesi, mağaza görselleri ve tanıtım metni.
5. İsim kontrolü: TÜRKPATENT ve WIPO.
6. Google Play geliştirici hesabı (tek seferlik 25 $).
7. **Kapalı test:** En az 12 kişi, 14 gün kesintisiz. Hatalar toplanıp düzeltilir.
8. Üretim yayını kademeli: %5 → %20 → %100. Çökme oranı izlenir.

### ADIM 7 — Takip ve yönetim
- Crashlytics (çökme raporları), Analytics (oyuncu nerede bırakıyor), Remote Config (APK çıkarmadan fiyat/etkinlik değiştirme), bildirimler (FCM).
- **Yönetim paneli:** Oyuncu arama, bakiye görme/düzeltme, banlama, etkinlik ve fiyat ayarı. Panelix deneyimi işe yarar.
- Destek e-postası, isim ve sohbet filtresi.

### ADIM 8 — Oyunu büyütmek
- Yeni oyuncu için eğitim maçı.
- Arkadaş listesi, kodla özel oda, kulüpler, arkadaş davet ödülü.
- Daha kaliteli sesler ve menü müziği (boyut bütçesi: 60–100 MB'a kadar yer var).
- Diller: İngilizce önce, sonra Arapça ve Hintçe.
- Yeni modlar ve sezonluk etkinlikler; yeni masa ve ıstaka paketleri (Furkan'ın görselleriyle).

### Her sürümde izlenen yol
1. İstenen iş yapılır (başka ayar bozulmaz).
2. Testler: tüm eski testler ve yeni testler (ekran görüntüsüyle kontrol).
3. Commit → push → CI → `surum-N`.
4. Furkan'a: indirme bağlantısı, ekran görüntüsü, kısa değişiklik listesi.
5. Bu not defteri güncellenir.
