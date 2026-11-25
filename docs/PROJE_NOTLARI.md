# Blackball Arena — Proje Not Defteri

Bu dosya, yeni bir sohbet açıldığında her şeyi baştan anlatmaya gerek kalmasın diye tutulur.
Yeni oturumda Claude'a ilk mesaj olarak şunu yaz: **"docs/PROJE_NOTLARI.md dosyasını oku, oradan devam et."**

Son güncelleme: 25 Kasım 2026 · Son sürüm: **surum-71**

---

## 1. Proje özeti
- **Oyun:** Blackball Arena (eski adları: 8 Blackball Arena, Bilardo Ustası). Mobil 8 top bilardo, Play Store'a çıkacak.
- **Sahibi:** Furkan. Sadece telefondan çalışıyor, bilgisayar yok. Türkçe konuşulur.
- **Depo:** github.com/furkankaraman755-dotcom/bilardo-ustasi (depo adı değişmedi)
- **İndirme:** Her sürüm `releases/download/surum-N/BilardoUstasi.apk`
- **Örnek alınan oyun:** 8 Ball Pool

## 2. Kullanıcının kalıcı kuralları
1. **"Bekle / başlama / not al"** denirse sadece not alınır. İş ancak **"başla"** (veya "yap") denince yapılır.
2. **Başka hiçbir şeyin ayarı bozulmaz.** Sadece istenen değişir.
3. **Ekranlar kullanıcının görsellerine birebir olur.** Görsel **parçalanarak** kullanılır; kodla çizilmiş taklit istemiyor ("acemice" buluyor). Ekranlar tam ekran olur, sayılar canlı, butonlar çalışır.
4. Gerçek kişi benzerliği ve telifli karakter (Naruto, Goku vb.) yapılmaz.
5. Masa görselleri toplu gelirse "yap" denince soru sormadan her biri ayrı tema olarak eklenir.
6. Play Store öncesi: TEST kilit açmaları ve 10B test parası kaldırılmalı.
7. İsim TÜRKPATENT/WIPO'da kontrol edilmeli (hatırlat).
8. Yeni APK kurmadan önce eskisi silinmeli (test imzası kullanılıyor).

## 3. Altyapı
- **Kod:** Tek dosya `index.html` (~0,56 MB, ~5300 satır). HTML5 + JavaScript, Canvas 2D. Fizik motoru tamamen bizim.
- **Görseller:** `a/` klasöründe ~110 WebP ve 3 MP4 (kutu efektleri). Toplam ~4,6 MB. Görseller artık HTML'e gömülmüyor, `a/xxxx.webp` yoluyla yükleniyor.
- **Android:** Capacitor 8 (WebView). `native/MainActivity.java` tam ekranı ve geri tuşunu yönetir; `native/res` uygulama simgeleri.
- **Derleme:** `.github/workflows/build.yml`. Her push'ta bulutta APK derlenir, `surum-N` olarak yayınlanır. `index.html` ve `a/` klasörü `www/` içine kopyalanır.
  - Maven 429 hatası verirse: `gh api -X POST repos/furkankaraman755-dotcom/bilardo-ustasi/actions/runs/<id>/rerun`
- **Paket adı:** `com.bilardoustasi.oyun`. Play Store'dan önce kalıcı ad seçilmeli, öneri `com.blackballarena.game`.
- **Boyut:** APK 9,2 MB. Kullanıcı 60–100 MB'ı tavan olarak kabul ediyor.
- **Kayıt:** Her şey telefonda, `localStorage`'daki `save` nesnesinde. Sunucu henüz yok.

## 4. Kodun yapısı (index.html)
- **Ana betik:** Oyunun çekirdeği. `save`, `TABLES`, `ROOMS`, `ALL_CUES`, `LEAGUES`, `BOXES`, `show()`, `startGame()`, `gameOver()`, `drawTable()`, `drawCue()`, `resize()`, `loop()`.
- **Sona eklenmiş betikler:** Eski fonksiyonları sarmalayarak (override) özellik ekleyenler. Yeni iş de çoğunlukla bu şekilde eklenir, böylece eski kod bozulmaz. Başlıcaları:
  - `curIcons`: 💵 yerine banknot görseli. `.chip` CSS'i ile 🪙 yerine B çip görseli.
  - `lifecycle`: 30 sn'den uzun arka planda kalırsa yeniden yükler.
  - `antiCheat`: `save.live`; maçtan kaçmak = yenilgi.
  - `bbaLog`: Hata kaydı. Ayarlar → Hakkında ekranında görünür.
  - `ensureScreen`: Siyah ekran koruması.
  - `chipFly2`: Çip uçuş animasyonu. Görünen çip sayacına uçar.
  - `feeGuard`: Giriş ücreti güvenliği. `save.pendFee`, maç açılamazsa iade.
  - `selfHeal`: Oyun ekranı ölçülerini düzeltir.
  - `freeGame`: Maçtan çıkınca bellek boşaltır.
  - `imgTables`: Resimli masalar. `TBL_SRC` / `TBL_IM`, `drawTable` sarmalayıcı.
  - İstaka standardı: `cueStdDraw` / `cueStdList`. Tembel çizim (IntersectionObserver).
  - `CUE_SHORT`: Kısa ıstaka isimleri.
  - Lig sistemi: `lgCredit`, `lgTick`, `renderLead`, `openLead`, `leadGoBack`.
  - `bbaBack`: Android geri tuşu.
  - `boxFx`: Sürpriz kutu videoları.
  - `ofFit` / `.of5`: Özel Teklif kartı.
- **Görsel ekranlar:** Tasarım koordinatlarıyla kuruludur (`--x/--y/--w/--h`), `--k` ile ölçeklenir, `fullFit` ile tam ekrana gerilir.

## 5. Oyun içeriği (şu an)
- **Ekranlar:** Giriş (misafir), ana menü (siyah-altın, kullanıcı görseli), profil (tam ekran), Ayarlar (7 sekme), Avatar Seç (14 resim, 9 renk), Hediyeler (Efsane Sandıklar, Şans Çarkı, Gizemli Kartlar, Altın Atış, Günlük Hazine), Mağaza (Özel Teklif, Sürpriz Kutuları, Çip ve Nakit, Efsane Sandıklar, Masalar), İstakalar (6 sekme), Liderlik, Gelen Kutusu, Görevler.
- **Ülke masaları (1'e 1):** 17 oda. Kazanılan ödül = 2 × giriş, net kazanç = giriş ücreti.
  - Portekiz 250 · İtalya 1K · Fransa 4K · Hollanda 5K · Brezilya 10K · Japonya 50K · Mısır 100K
  - İspanya 250K · Almanya 500K · İngiltere 1M · Rusya 2,5M · Kore 5M · Amerika 10M
  - Dubai 25M · Monako 50M · Las Vegas 100M · İstanbul 250M
  - 1'e 1'de oyuncunun seçtiği masa değil, ülkenin kendi (kodla çizilmiş) masası kullanılır.
- **Turnuva:** Giriş 1000, ödül 7500, 3 tur.
- **Masalar (13):**
  - Klasik 3 (kodla çizilmiş, ortada "8 BLACKBALL ARENA" baskısı): Turnuva (varsayılan), Saray Halısı, Mor Saray
  - Resimli 10: Pembe Saray, Zehir Neon, Buz Kristal, Kızıl Ateş, Zümrüt Saray, Gece Moru, Elektrik Mavi, Kara Altın, Gümüş Saray, Lav Alevi
  - Resimli masalarda görsel, çuha kenarı oyun alanına ve cepler fizik ceplerine oturacak şekilde hizalanır (Python ile önceden). Çince yazı ve "AI tarafından oluşturulan içerik" filigranı temizlendi.
- **İstakalar (84):** Hepsi Ejder ölçüsünde, kabza solda, uç sağda, ortalı. Kısa isimler (Ejder, Volkan, Fırtına, Galaksi, Zümrüt…). MAX ejderhalar gökkuşağı efektli.
- **Kutular:** Nadir 5/14 · Destansı 16/44 · Efsanevi 33/89 (1 tane / 3 tane, nakit). Sürpriz Kutuları açılışı kullanıcının videosundan.
- **Özel Teklif:** FIRSAT kartı (kullanıcı görseli). Şu an normal Destansı fiyatı. **Fiyatlar sonra konuşulacak**, günlük yarı fiyat indirimi devre dışı.
- **Lig (21 günlük dönem):**
  - Başlangıç 17 Kasım 2026 00:00 (TR). Puan = net kazanç (ödül − giriş), maç başına bir kez sayılır.
  - Eşikler: Novice 0 · Pioneer 30K · Nova 150K · Rogue 300K · Valor 1M · Astra 3M · Zenith 10M · Dominion 30M · Eclipse 100M · Paragon 300M
  - Dönem sonu ödülü: eşiğin %10'u çip + 1 elmas. Puan sıfırlanır, geçmiş saklanır.
  - Sunucu planı: `docs/lig-sunucu.md`
- **Para simgeleri:** Çip = siyah-altın taçlı B çip. Nakit = yeşil banknot destesi (kullanıcı görselleri).

## 6. Sürüm geçmişi (özet)
- **20 Kasım:** Fizik (3 aşama), gerçek vuruş hareketi, nişan/MAX ıstaka, 16+6 ıstaka, ülke masaları ve ligleri, sinematik eşleşme, XP/unvan (1000 seviye), sohbet/hediye, mor-altın tema.
- **21 Kasım gece:** Görsellerden parçalı ekranlar: menü, giriş, profil, liderlik, ayarlar, avatar, hediyeler. Ad Blackball Arena oldu.
- **surum-63:** Simge C, siyah ekran ilk düzeltme, 30 sn kuralı + hile koruması, yeni çip/nakit simgeleri, pot çip yığını.
- **surum-64:** İstaka standardı, kısa isimler, simgeler her yerde.
- **surum-65:** 6 resimli masa.
- **surum-66:** Siyah ekran koruması + hata kaydı, yeni çip uçuşu, Destansı kutu görseli.
- **surum-67:** Grafik bellek düzeltmesi.
- **surum-68 (sağlamlık):** Görseller dosyalara taşındı (HTML 5,4→0,5 MB), bellek tasarrufu, giriş ücreti iadesi, ekran kendini düzeltir.
- **surum-69:** 9 masa (5 yenilendi + 4 yeni), Özel Teklif FIRSAT kartı.
- **surum-70:** 21 günlük lig, geri tuşu/Android geri, kutu açılış efekti.
- **surum-71:** Demo masalar kaldırıldı; klasik 3 masa BLACKBALL baskısıyla geri geldi; mağaza masa adı hatası düzeldi.

## 7. Yaşanan hatalar ve dersler
- **Kodla çizilen tasarımlar:** Reddedildi. Çözüm: kullanıcının görselini parçala (OpenCV inpaint ile yazı silme, canlı yazıyı HTML ile üstüne koy).
- **Ekranlar tam ekran değildi:** `fullFit` ile germe eklendi.
- **Simgeler "taştı":** Sonunda kullanıcının kendi para çubuğu görseli kullanıldı.
- **Siyah ekran (ilk açılış) ve dev/bozuk oyun ekranı:**
  - En güçlü sebep WebView grafik belleğinin dolması (tek dosyada 5 MB gömülü görsel, 84 ıstaka çizim alanı, body'ye transform hilesi).
  - Çözüm: görseller dosyaya taşındı, tembel çizim, maçtan çıkınca bellek boşaltma, açılış zinciri try/catch, `ensureScreen`, `resize` doğrulama, hata kaydı.
  - Tekrar olursa: silmeden önce Ayarlar → Hakkında'daki "Hata kaydı"nın fotoğrafı istenecek.
- **Çip kesildi ama maç açılmadı:** `feeGuard` eklendi. Maç başlamazsa 16 sn içinde ya da bir sonraki açılışta iade edilir; iptalde çift iade olmaz.
- **Çipler sola uçuyordu:** Hedef, mağazadaki gizli dev kapsayıcıydı. Artık görünen `.cv` öğesine uçuyor; sabit katman olduğu için sayfa büyümüyor.
- **Mağaza masa adı ekranın ortasında bozuk görünüyordu:** Başka bir global `.nm` CSS kuralı yüzündendi. `.item .info .nm` ile kapsamlandı.
- **Playwright testinde `file://` ile canvas `getImageData` kirleniyor:** Testler `http://localhost` sunucusuyla yapılmalı.
- **Kutu satın alınınca ödül penceresi 1,35 sn gecikmeli gelir** (açılış efekti). Testlerde buna göre beklenmeli.
- **Not:** surum-70 açıklamasında "Dubai 25 bin" yazıldı; doğrusu Dubai girişi **25 milyon**, kazanınca +25.000.000 lig puanı.

## 8. Test yöntemi (geliştirici için)
- Playwright + `/usr/bin/google-chrome`. Giriş: `#lname` doldur, `#lgGuest` tıkla.
- Yerel sunucu: `index.html` ve `a/` klasörü bir klasöre kopyalanıp `python3 -m http.server` ile açılır.
- Testler `/home/claude/test/t*.py` (bu ortama özel): fizik, menü, mağaza, lig, ücret/iade, geri tuşu, kutu efekti vb.
- Bellek ölçümü: CDP `Performance.getMetrics` ve sayfadaki canvas toplamı.

## 9. Bekleyen işler
1. **Ülke masaları (1'e 1):** Kullanıcı fotoğraf gönderebilir. Ayrıca seçilen masanın 1'e 1'de de kullanılıp kullanılmayacağına karar verilecek (3 seçenek sunuldu).
2. **Özel Teklif fiyatları:** Karar bekleniyor.
3. **Yeni özgün ejderha ıstakaları:** Kullanıcı kendi görsel aracıyla üretip gönderecek, otomatik olarak standarda oturacak.
4. **Firebase (online):** Kullanıcı Firebase'i Panelix'ten biliyor. Sıra:
   1. Giriş (Google/Facebook/misafir) + bulut kayıt
   2. Sunucuda ekonomi (giriş/ödül/kutu/lig)
   3. Online 1'e 1 (vuruş verisi senkronu, sunucu aynı fizik koduyla doğrular, bot yedeği)
   4. Google Play ödeme + AdMob ödüllü reklam + onay (KVKK/GDPR)
   5. Play Store hazırlığı: AAB, sabit imza, gizlilik politikası, Veri Güvenliği, yaş derecesi, kutu olasılıkları, 12 kişi/14 gün kapalı test, test parasının kaldırılması
   6. Sosyal: arkadaş, kulüp, bildirim; modlar (9 top), eğitim maçı, ses/müzik, İngilizce
   7. Yönetim paneli (Panelix deneyimi), Crashlytics, analitik
   - Kullanıcıdan gerekenler: Firebase projesi (Blaze planı), Android uygulama kaydı + `google-services.json`, GitHub için dağıtım anahtarı, kalıcı paket adı kararı.

## 10. Ayrı projeler (kullanıcının diğer fikirleri)
- Araba oyunu (hazır altyapı denemesi)
- Okey oyunu (standart + VIP)
- Panelix (Firebase'li sistem)
