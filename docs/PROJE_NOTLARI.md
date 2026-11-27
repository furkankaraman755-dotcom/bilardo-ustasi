# Blackball Arena — Proje Not Defteri

Bu defter, yeni bir sohbette her şeyi baştan anlatmamak için tutulur.
Yeni sohbette ilk mesaj: **"docs/PROJE_NOTLARI.md dosyasını oku, oradan devam et."**

Son güncelleme: 27 Kasım 2026 · Son sürüm: **surum-78** · Sıradaki iş: **K-00 Profesyonellik denetimi** (bkz. Bölüm 7)

**İçindekiler**
1. Projenin kimliği ve Furkan'ın kuralları
2. Teknik altyapı (kod, kayıt, ekranlar, testler, derleme)
3. Şimdiye kadar ne yaptık (19 Kasım → surum-78, tarih sırasıyla)
4. Oyunun içeriği (masalar, fiyatlar, sandıklar, lig)
5. Yaşanan hatalar ve dersler
6. Konuşulan kararlar (maliyet, sunucu, paket adı)
7. Bundan sonra ne yapacağız (bekleyen kararlar, eksikler listesi, sıra)

---

## BÖLÜM 1 — Projenin kimliği

| Konu | Bilgi |
|---|---|
| Oyunun adı | **Blackball Arena** (önce "Bilardo Ustası", kısa süre "8 Blackball Arena") |
| Tür | Mobil 8 top bilardo; online ve çok oyunculu olacak |
| Hedef | Google Play Store, sonra global (milyonlarca indirme hedefleniyor) |
| Örnek alınan | 8 Ball Pool |
| Sahibi | Furkan. Sadece telefondan çalışıyor, bilgisayar yok |
| Önemi | Furkan'ın sözü: "bu oyun umudumuz, son çaremiz". Para az; her harcama dikkatle seçilir |
| Depo | github.com/furkankaraman755-dotcom/bilardo-ustasi |
| APK indirme (test) | `https://github.com/furkankaraman755-dotcom/bilardo-ustasi/releases/download/surum-N/BilardoUstasi.apk` — test modu açık (5 milyar çip, kilitler açık) |
| APK indirme (yayın hâli) | `…/releases/download/surum-N/BlackballArena-yayin.apk` — test modu kapalı, gerçek oyuncu gibi (1.000 çip), ayrı kayıt |
| Paket adı | **`com.blackballarena.game`** (kalıcı, surum-72'den beri; eskisi `com.bilardoustasi.oyun`) |
| Tasarım dili | surum-76'dan beri: mavi ana menü + altın; giriş/mağaza/masalar Furkan'ın 3B görselleri. Eski ekranlarda siyah-altın-mor |
| Para birimleri | **Çip** (oyun parası), **Nakit / Dolar** (yeşil banknot; kutular ve sandıklar), **Elmas** (lig ödülü) |
| Sunucu | Henüz yok. Karar: **Hetzner**; Firebase'in rolü sonra konuşulacak |

### Furkan'ın kalıcı kuralları
1. **"Bekle / başlama / not al"** → sadece not alınır. **"Başla" / "yap"** → uygulanır.
2. **Başka hiçbir şeyin ayarı bozulmaz.** Sadece istenen değişir.
3. **Ekranlar Furkan'ın görsellerine birebir yapılır:** görsel parçalanır, yazılar silinip canlı yazı konur, ekran tam ekran olur, **her düğme çalışır**. Kodla çizilmiş taklit "acemice" bulundu, istenmiyor. Furkan "hepsi 3B olsun" dedi.
4. Masa görselleri toplu gelir; "yap" denince soru sormadan her biri ayrı tema olarak eklenir. Masalar ekranında mevcut masaların hepsi isimleriyle görünür.
5. Gerçek kişi benzerliği ve telifli karakter (Naruto, Goku vb.) yapılmaz.
6. Yeni APK kurmadan önce eskisi silinmeli (şu an test imzası kullanılıyor).
7. Test parası, kilit açmalar ve kısayollar tek bayrağa bağlı (`window.BBA_DEV`); yayın APK'sında kapalı. İsim TÜRKPATENT/WIPO'da kontrol edilecek.
8. Furkan görsel üretir (kendi yapay zekâ aracıyla). Claude resim üretmez; görselleri oyuna yerleştirir, temizler, parçalar ve hizalar.
9. Büyük işlerde **denetçi alt ajan** çalışır, işi adım adım izler, hata görünce uyarır. **Denetçi Furkan'a haber verilmeden asla kapatılmaz;** görevi bitince Furkan'a söylenir.
10. "✅ işareti yetmez": görev bitti demek, oyunun o kısmının **eksiksiz ve profesyonel** olması demek (AŞAMA K bunun için var).
11. Her işten sonra: test → commit → push → CI (`surum-N`) → indirme bağlantısı. Sonra bu defter ve `YOL_HARITASI.md` güncellenir. Başka sohbet de çalışıyor olabilir: işe başlamadan `git pull`.

---

## BÖLÜM 2 — Teknik altyapı

### Kod
- **Oyun kodu:** Tek dosya `index.html` (~0,63 MB, ~5850 satır). HTML5 + JavaScript, Canvas 2D. Fizik motoru tamamen bize ait.
- **Görseller:** `a/` klasöründe 135 dosya (WebP + 3 MP4 kutu efekti). HTML'e gömülmez, dosya yoluyla yüklenir. Yeni V6 görsellerinin adı içeriğin sha1'inin ilk 12 harfi.
- **Yöntem:** Yeni özellik = dosyanın sonuna eklenen betik; eski fonksiyonlar sarmalanır (önce yenisi çalışır, sonra eskisi çağrılır). Eski kod silinmez, bozulmaz.
- **Yorum kuralı:** Satır içinde sadece `/* */`. `//` tek satırlık kodun devamını yutuyor (surum-73'te yaşandı).
- **Önemli kod parçaları:**
  - Çekirdek: `save`, `TABLES`, `ROOMS`, `ALL_CUES`, `LEAGUES`, `BOXES`, `show()`, `startGame()`, `gameOver()`, `drawTable()`, `drawCue()`, `resize()`, `loop()`
  - Para ve güvenlik: `antiCheat` (maçtan kaçan kaybeder), `feeGuard` (giriş ücreti iadesi, 16 sn bekçi), `_feeVoid`, `goDone`, `_boxLock`, `save.pendRw` (yarım kalan ödül), `cleanName`
  - Kararlılık: `lifecycle` (30 sn arka plan → yeniden başlat), `ensureScreen` (siyah ekran), `selfHeal` (ölçü), `freeGame` (bellek)
  - Görsel: `chipFly2`, `imgTables`, `cueStdDraw`, `boxFx`, `ofFit`, `fullFit`
  - Lig: `lgCredit`, `lgTick`, `renderLead`, `openLead`, `leadGoBack`
  - Geri tuşu: `bbaBack` (önce pencere kapanır, ana menüde uygulama arka plana)
  - Özel Teklif: `OFFER_PRICE`, `buyOffer`

### Kayıt (telefonda, `localStorage`)
- İki yuva: `KEY` (ana) ve `KEY_B` (bir adım geride yedek). Bozuk ana kayıt `KEY_X`'e taşınır, yedekten açılır, "Kayıt kurtarıldı" notu düşer.
- Yayın sürümünde anahtarlara `_yayin` eklenir (`bilardo_ustasi_v1_yayin`), test ve yayın kayıtları karışmaz.
- `validSave` (doğrulama), `saveRepair` (NaN vb. onarım), `bbaTrim` + `BBA_LIM` (listelere üst sınır), `persist` (hafıza dolarsa temizleyip tekrar dener, olmazsa uyarır).
- Sıfırla / yedekten yükle: `window._bbaNoSave=1` (sayfa kapanırken eski kayıt geri yazılmasın).
- Yedek: yedek kodu, dosyaya kaydet (İndirilenler/BlackballArena/…txt), dosyadan yükle, paylaş (Drive/WhatsApp). Hepsi `validSave`'den geçer.
- **Hesaplar (surum-76):** `bba_acc` içinde, telefonda. Şifre PBKDF2-SHA256, 60.000 tur, tuzlu; açık saklanmaz. "Beni hatırla" kullanıcı adı `bba_remU`. Hesaplar henüz ayrı kayıt değil (tek `save`). Sunucu gelince taşınacak.
- Dil: `bba_lang` (tr, en, es, de, fr, ar).

### Teşhis
- `bbaLog` (son 50 hata), `bbaIz` (açılış izi; ilk 12 satır korunur, önceki açılış `bba_iz_onceki`), `bbaDevice` (Android, model, WebView, bellek), `bbaReport()`.
- Ayarlar → Hakkında → 📋 Hata raporunu kopyala / 📤 Paylaş. Oyuncu adı ve bakiye raporda yok.
- `BBA_SURUM`: CI `__SURUM__`'u derleme numarasıyla değiştirir.

### Telefon köprüsü
- `native/MainActivity.java`: tam ekran, Android geri tuşu, `setTextZoom(100)` (telefonun yazı boyutu oyunu bozmasın).
- `BbaNative` Capacitor eklentisi (`saveText`, `shareText`); `super.onCreate`'ten önce kaydedilir. JS'te `bbaNat()`, `bbaSaveFile()`, `bbaShare()`, `bbaCopy()`.

### V6 katmanı (surum-76: Furkan'ın 12 görseli)
- Kod: `index.html` sonunda `/* ===== V6 */` stil + betik bloğu. `IMG` haritası görsel adlarını tutar.
- Tasarım ölçüsü **1600×900**. `.v6` kapsayıcısı, `v6fit()` genişliğe göre ölçekler (`sx = ekran genişliği / 1600`); üst/alt güvenli bant `data-t` / `data-b`.
- `.v6h` = görselin üstündeki görünmez dokunma alanları; `.v6t` = canlı yazılar; `.v6m` = tam ekran görsel pencereler.
- **Dokunuş kuralı (surum-77 dersi):** tam ekran kaplayan katmanlar `pointer-events:none`, düğmeler `.v6 .v6h{pointer-events:auto!important}`. Genel `button` CSS'i `.v6 .v6h` için `!important` ile sıfırlanır (yoksa mor düğme görünür).
- Sınıf adları `v6` önekli (eski `.win/.nm/.pl/.fr/.bd/.lk` kurallarıyla çakışmasın).
- `inset:0` yerine açık `left/top/right/bottom` (eski WebView'lar `inset`i tanımıyor).
- Fonksiyonlar: `buildLogin/openGiris/openSifre/openUye/openDil`, `buildMenu/refreshMenu/quickPlay`, `buildShop/setTab/tlBuy/claimGift/buyChest/openDailyChest`, `buildTables/renderTables6/openTables6`.
- Sarmalananlar: `openShop` (`'free'` → eski ücretsiz ödüller, `'tables'` → 3B Masalar, kutu/teklif/paket eşlemesi), `show`, `refreshCoins`, `bbaBack`. Eski `#shopTabs` gizli.
- Dışa açık: `window.V6API`, `SHOP6`, `openShop6`, `openTables6`, `openDailyChest`.
- **3B masalar:** `homog(w,h,quad)` → CSS `matrix3d`. Üstten çizilmiş masa resmi görseldeki 3B gövdeye perspektifle oturtulur (`BIGQ` büyük önizleme, `CARDQ` kartlar). Yeni masa eklenince kendiliğinden 3B olur.
- RTL (Arapça): `[dir=rtl] .v6t.l{direction:rtl;justify-content:flex-end}`, şifre alanlarında sağ boşluk 70.
- **Efsane Sandıklar ekranı (`#free6`, surum-78):** dosya sonunda `FREE6` bloğu. `window.V6UI` (V6'nın el/hot/txt/toast/fit parçaları) ile kurulur. `openShop('free')` → `openFree6()`. Ödül mantığı eskisiyle aynı (`save.free`, `FREE`). Altında **SANDIKLARIM** (4 yuva: Kilidi Aç / Sırada / süre → elmasla aç / AÇ!). `renderSlots` ve `giftCounts` sarmalandı.
- **Eski `#shop` ekranı artık hiçbir yoldan açılmaz.** Kodda duruyor (silinmedi), sekme çubuğu `#shop #shopTabs,#shopTabs{display:none!important}` ile gizli.
- Görsel temizleme araçları (Claude'un çalışma klasöründe, depoda değil): `sil.py` (silme / yatay-dikey doldurma), `warp.py`, `assets.py`, `map.json`.

### Test modu
- `window.BBA_DEV=true;/*DEV*/` kaynakta açık. Bağlı olanlar: test parası (5B çip + 10B), `TEST_UNLOCK` (masa kilitleri, bütün ıstaka/masa), menü sayacına 5 dokunuş kısayolu. Hakkında'da ve raporda "TEST MODU" yazar.
- CI yayın APK'sında `sed` ile `false` yazar ve `grep` ile doğrular.

### Testler (`tests/`, pytest + Playwright, **45 test**)
| Dosya | Ne sınar |
|---|---|
| `conftest.py` | `Game` yardımcısı: sabit tohum (mulberry32), zaman hızlandırma (≥5000 ms süreler hızlandırılmaz), temiz `bba_err`; `no_errors` hata kaydını da kontrol eder |
| `test_acilis` | Açılış, siyah ekran, betik hataları |
| `test_kurallar` | 8 top kuralları, faul, maç sonu |
| `test_ekonomi` | Giriş ücreti, ödül, iade, oda maçı |
| `test_oduller` | Kutu, kart, çark, gelen kutusu |
| `test_kayit` | Çift yuva, bozuk kayıt, yedek, sıfırlama |
| `test_guvenlik` | İsim temizleme, yedek kodu alanları |
| `test_rapor` | Hata raporu, iz, cihaz bilgisi |
| `test_devmode` | Test modu açık/kapalı farkı |
| `test_gorunus` + `gorunus.py` | Ekranlar önceki commit'le piksel piksel karşılaştırılır (eşik 25 piksel). Bilerek görünüş değiştiren commit'e **`[görünüş]`** yazılır |
| `test_v6` | Yeni giriş, menü, mağaza, masalar ekranlarının işlevleri; pot çipi görseli ve miktarı; amblem/giriş efekti ve Android simge boyutları |
| `test_dokunus` | **Gerçek parmak dokunuşu** (`touchscreen.tap`): yeni ekranlardaki 108+ düğmenin her biri; her dokunuştan önce ekran sıfırlanır. Efsane Sandıklar toplama akışı ve "eski mağaza hiçbir yoldan açılmaz" testi |
- Ayrıntı: `tests/OKU.md`. Yeni düzeltilen her hataya bir test eklenir.

### Derleme (CI) — `.github/workflows/build.yml`
1. **test işi:** pytest 9.1.1 + playwright 1.63.0 + pillow 12.3.0; `fetch-depth: 2`, `BBA_PREV_REF=HEAD~1` (görünüş karşılaştırması). Geçmezse APK derlenmez.
2. **build işi** (`needs: test`): `__SURUM__` → derleme numarası; Capacitor 8 + Gradle → **BilardoUstasi.apk** (test).
3. Aynı işte `BBA_DEV=false` yazılır → `cap copy` → **BlackballArena-yayin.apk**.
4. İki dosya `surum-N` etiketiyle Releases'e yüklenir.
- Sadece not/belge değişikliğinde commit mesajına `[skip ci]`.
- Maven 429 hatası olursa iş yeniden çalıştırılır (`gh api -X POST …/actions/runs/<id>/rerun`).
- APK ~9–10 MB (tavan 60–100 MB).

### Belgeler
- `docs/PROJE_NOTLARI.md` — bu defter (ne yaptık).
- `docs/YOL_HARITASI.md` — fazlar ve büyük plan (tek plan kaynağı).
- `docs/GOREV_HARITASI.md` — oturum oturum somut görevler, "Sıradaki görev — NEREDE KALDIK".
- `docs/CIHAZ_TEST_LISTESI.md` — telefonda 5 dakikalık kontrol (15 madde + A–D).
- `tests/OKU.md` — testlerin listesi.

---

## BÖLÜM 3 — Şimdiye kadar ne yaptık (tarih sırasıyla)

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


### 25 Kasım — surum-72
- **Kararlar:** 1'e 1'de ülke masası kalır (seçilen masa 1'e 1'e uygulanmaz). Özel Teklif %30 indirimli. Kalıcı paket adı `com.blackballarena.game`.
- **Özel Teklif fiyatı:** Destansı Kutu 1 tane **11**, 3 tane **31** nakit (`OFFER_PRICE`, `buyOffer`). Sürpriz Kutuları'ndaki normal fiyat 16/44 aynı kaldı. Şimdilik günlük sınır yok.
- **Paket adı değişti:** `capacitor.config.json`, `native/MainActivity.java`, `build.yml`. Yeni APK eski uygulamanın yanına ayrı uygulama olarak kurulur; eski "Blackball Arena" silinmeli.

### 25 Kasım — surum-73 (hata avı: 22 düzeltme)
Furkan: "kodu sıfırdan analiz et, bütün hataları bul, tek tek düzelt ve test et; bir alt ajan seni izlesin." Kod baştan tarandı. Denetçi alt ajan bağımsız tarama yaptı, her düzeltmeyi ayrıca test edip onayladı. Testler tarayıcıda (Playwright + Chrome); 2 kişilik kural simülasyonunda binlerce atış ve fizik fuzz testi.
- **Kritik**
  - Pes et/ayrıl sırasında yuvarlanan 8 → maç hem kayıp hem galibiyet sayılıyor, ödül veriliyordu. Çözüm: `goDone` bayrağı (gameOver maç başına bir kez) ve `endShot` başında `if(over)return`.
  - Resimli avatar seçen oyuncuda her açılışta `AV_ART` TDZ hatası; büyük betiğin kalanı çalışmıyordu (`fullFit`, lifecycle ve antiCheat devre dışı). Siyah/bozuk ekran şikâyetiyle ilgili olabilir. Çözüm: `window.AV_ART`, açılış çağrısı try/catch içinde.
  - Ayarlar → "İlerlemeyi sıfırla" ve "Yedekten geri yükle" hiç çalışmıyordu: sayfa kapanırken `persist()` eski kaydı geri yazıyordu. Çözüm: `window._bbaNoSave`.
- **Para / ödül**
  - Sürpriz Kutusu efekti sürerken ikinci basışta nakit iki kez düşüyordu → `_boxLock`.
  - Gizemli Kart kazınmadan kapatılırsa ya da çark dönerken oyun kapanırsa ödül gidiyordu → ödül `save.pendRw` olarak hemen kayda geçiyor; yarım kalırsa açılışta gelen kutusuna veriliyor.
  - Ücret zaman aşımıyla iade edildikten sonra eşleşme yine maç açabiliyordu (bedava maç) → `_feeVoid`.
  - 9 Top / Kılavuzsuz odalarında 20. galibiyet yanlışlıkla ülke ıstakası veriyordu → sadece ülke odaları rozet veriyor.
  - Gelen kutusu 20 mesajı aşınca alınmamış ödülleri siliyordu → ödüllüler korunuyor.
- **Güvenlik**
  - Oyuncu adındaki HTML kodu çalışıyordu → `cleanName` (< > & " ' ` \ temizlenir, en fazla 14 karakter).
  - Yedek kodundan gelen avatar, ID ve gelen kutusu alanları yüklemede temizleniyor.
- **Küçükler**
  - Turnuva eşleşme ekranı giriş ücretini 3.750 gösteriyordu (doğrusu 1.000); 2. ve 3. turda sadece ödül görünüyor.
  - Kutu ödül penceresi başka pencereyle ezilince çıkan hata giderildi.
  - "Kopyalandı" mesajı artık kopyalama başarısızsa çıkmıyor (`bbaCopy`).
  - Altın Atış sonucunda geri tuşu menüye götürüyor; cep bilgisi yoksa NaN koruması.
  - Yapay zekâ hedef bulamazsa çökmüyor.
  - Görev metni "Bursa" yerine "İtalya veya üstü".
  - Menüdeki sandık yuvaları sadece yazı değişince yeniden çiziliyor.
  - 780 px ekranda ıstaka etiketi kesilmiyor.
  - Kayıtta artık olmayan ıstaka/masa seçiliyse açılışta Başlangıç ıstakası / Turnuva masasına dönülüyor.
- **Bilerek bırakılanlar:** `openGifts` iki kez tanımlı (ölü kod, zararsız). Lig puanı sadece kazançla artıyor (tasarım kararı). Yedek kodu ile bakiye değiştirilebiliyor (sunucu ekonomisi, ADIM 3 ile çözülecek).

### 26 Kasım — Görev haritası (GOREV_HARITASI.md) başladı
Furkan: "görev haritasına disiplinli şekilde uy." Haritadaki eksik/hatalı görevler sırayla yapıldı. Biten: **H-01…H-05, H-08, H-09, 0-01…0-04, 1-01…1-03.**

### 26 Kasım — surum-74 (güvenlik ağı)
- **H-01/H-02 (0-01):** Çift yuvalı, doğrulamalı kayıt; bozuk kayıtta yedekten açılış + "Kayıt kurtarıldı"; hafıza dolu olunca temizleyip tekrar deneme, olmazsa uyarı; NaN gibi bozuk değerler onarılır. Yedek kodu da `validSave`'den geçer.
- **H-03:** Bütün listeler için tek üst sınır kuralı (`BBA_LIM`, `bbaTrim`).
- **H-08:** Liderlik efekti çizim alanı ekrandan çıkınca boşaltılıyor (~4 MB).
- **0-02 + H-04:** Ayarlar → Hakkında → 📋 Hata raporunu kopyala / 📤 Paylaş (sürüm, cihaz, bu ve önceki açılışın izi, 3./10. saniyede ekran durumu, son 50 hata).
- **0-03:** Ayarlar → Güvenlik → 💾 Dosyaya kaydet, 📂 Dosyadan yükle (aynı doğrulama ve çift onay), 📤 Paylaş.
- **0-04:** `docs/CIHAZ_TEST_LISTESI.md`.
- **1-01:** `tests/` klasörü, 32 otomatik test; GitHub'da APK'dan önce çalışır.
- Denetçinin 5 uyarısı (NaN'da kaydın durması, geçersiz yedek kodu, iz gürültüsü, telefonda sahte "kaydedildi" mesajı, Capacitor eklenti erişimi) düzeltildi.

### 26 Kasım — surum-75 (1-02, 1-03, H-05)
- **1-03 / H-05:** Test modu tek bayrak `BBA_DEV`. CI artık iki APK veriyor: **BilardoUstasi.apk** (test) ve **BlackballArena-yayin.apk** (1.000 çip, kilitli masalar, ayrı kayıt).
- **1-02:** Görünüş testi: 23 ekran önceki commit'le piksel piksel karşılaştırılıyor.
- Ayarlar → Güvenlik: "Dosyaya yedek" etiketi düğmeye değmiyor. `setTextZoom(100)`: telefonun yazı boyutu oyunu bozmuyor.

### 26 Kasım — "✅ yetmez" kararı ve bekleme
- Furkan: "Görev haritası iyi hoş, tik yetmiyor; oyunun eksiksiz ve profesyonel olması lazım."
- Karar: `GOREV_HARITASI.md`'ye **AŞAMA K (Kalite ve profesyonellik)** eklendi. İlk iş **K-00 Profesyonellik denetimi** (oyun 8 Ball Pool ile ekran ekran karşılaştırılacak, ekran görüntülü eksikler listesi çıkacak, her eksik bir K görevi olacak).
- Furkan "bekle, başlama" dedi → K-00 ⏸. Nerede kalındığı haritaya yazıldı.

### 26 Kasım — surum-76 (Furkan'ın 12 yeni görseli: giriş, menü, mağaza, masalar)
- İlk 11 görsel geldi, Furkan "iptal, yeni fotoğraflar gelecek" dedi; sonra 12 görsel geldi: "masa ekranında mevcut masalar ve isimleri olsun, eksiksiz ve kusursuz, gerekirse parçalayarak, hepsi 3B."
- Bütün ekranlar görsellerden parçalandı (yazılar silindi, değişen yazılar canlı). Eski ekranlar silinmedi; yeni katman üstte, eski düğmelerin işlevleri çağrılıyor. (Teknik ayrıntı: Bölüm 2 → V6 katmanı.)
- **Giriş:** Giriş Yap / Üye Ol / Misafir / Google-Facebook-Apple (sunucu gelince) / ses / dil.
  - Pencereler: Giriş Yap (hata hâli ayrı görsel), Şifremi Unuttum, Üye Ol, Dil Seçimi.
  - Hesaplar şimdilik telefonda (PBKDF2). **6 dil** (tr, en, es, de, fr, ar; Arapça sağdan sola): şimdilik sadece giriş ekranları çevrili; oyunun geri kalanı 1-04 ile çevrilecek.
- **Ana menü (mavi):**
  - Canlı: isim, seviye, XP çubuğu, para, avatar, posta ve ıstaka rozetleri, Sezon, Günlük Sandık ve Özel Teklif süreleri.
  - **OYNA:** giriş ücreti bakiyenin en fazla **%15**'i olan en yüksek açık ülke masası (birikim tek dokunuşta gitmesin; hiçbiri uymazsa en ucuzu).
  - Dünya Çapında Oyna → ülke listesi. Arkadaşla Oyna → Özel Oyun. Gelişim → Profil. Masalar → 3B Masalar ekranı.
- **Mağaza (4 sekme):** Özel Teklifler, Çip Paketleri, Dolar Paketleri, Sandıklar (fiyatlar görseldeki gibi; Bölüm 4).
  - TL paketleri: test APK'sında onayla bedava, yayında "ödeme Google Play sürümünde".
  - Günlük Hediye ve Günlük Sandık: günde bir; reklam (AdMob) gelene kadar reklamsız.
  - Eski Sürpriz Kutuları ve Destansı Özel Teklif (11/31) arayüzden kalktı (kod duruyor). Hediyeler → Efsane Sandıklar eski ücretsiz ödül listesini açıyor.
- **Masalar ekranı:** Büyük 3B önizleme + kart sırası; 13 masanın hepsi isimleriyle. Karta dokun → önizle; KULLAN → seç.
- **Denetçinin bulduğu ve düzeltilenler:** OYNA en pahalı masayı seçiyordu (→ %15 kuralı); ses düğmesi çalışmıyordu (`applySound` yoktu → `applyVol`); Beni Hatırla kullanıcı adını tutmuyordu (`bba_remU`); sandıkta NaN (`!(save.cash>=cost)`); eksik rozetler; Arapça hizalama; mor düğmeler; Masalar ekranı ilk açılışta boş (önce kurulmuyordu); sınıf adı çakışmaları; modallarda sürüm yazısı; "Hesabın yok mu? Üye Ol" boşluğu.
- Testler: `test_v6.py` eklendi, sandık testi yeniden yazıldı, görünüş testine yeni ekranlar eklendi.
- Ara not (test): Oda maçı testinde kayıp dalı seviye ödülünü hesaba katmıyordu, ara sıra yanlış kırmızı veriyordu → üst sınıra `lv*250 + titleReward` eklendi.

### 26 Kasım — surum-77 (acil: "çoğu buton çalışmıyor")
- Furkan: "Çoğu butonların çalışmıyor, denetleyici ajanı aktif et, oyunun tüm eksiklerini tespit etsin, sen düzelt."
- **Sebep:** Mağazada tam ekran görünmez bir katman (`SU.layer`) Geri, sekmeler ve "+" düğmelerinin üstündeydi; parmak dokunuşu ona gidiyordu. Önceki testler `.click()` ile yapıldığı için bunu yakalayamadı.
- **Düzeltme:** katman `pointer-events:none`, düğmeler `pointer-events:auto!important; touch-action:manipulation`; V6 CSS'inde `inset` yerine açık kenarlar.
- **Yeni kalıcı test `tests/test_dokunus.py`:** yeni ekranlardaki 108+ düğmenin her birine gerçek dokunuş. Eski sürümde kırmızı, yenide yeşil. CI: 41 test geçti.
- Denetçi bütün oyunu taradı; dokunuşu engelleyen başka bir şey bulmadı. "Çalışmıyor gibi görünenler" listesi Bölüm 7'de.

### 26 Kasım (gece) — Furkan'ın 3 görsel isteği, "bekle"
- Pot çipi görseli (G-01), yeni uygulama amblemi (G-02), ödül alırken çıkan eski mor mağaza ekranı (G-03). Hepsi not alındı, görseller `docs/bekleyen_gorseller/`'e kondu.

### 27 Kasım — surum-78 (G-03, G-01, G-02)
Furkan: "Devam et." Denetçi alt ajan yeniden başlatıldı, önce bağımsız hazırlık taraması yaptı, sonra her işi ayrı test edip onayladı.
- **G-03 — Efsane Sandıklar yeni ekranda:**
  - Hediyeler → Efsane Sandıklar artık yeni mavi tasarımda kendi ekranını açıyor: Masalar görselinden başlık silinip gövdesi bulanıklaştırılan arka plan; satır çerçevesi, yeşil düğme, çip ve sandık mağaza görselinden parçalar. 1K / 2,5K / 5K Çip / Bronz Sandık, TOPLA, 30 dk bekleme, kilit, "✓ TOPLANDI", sıfırlanma süresi.
  - **Hata:** eski mağazanın sekme çubuğu gizlenemiyordu (eski CSS kuralı daha güçlüydü). Oyuncu bu yoldan eski Özel Teklif'ten (11/31) ve eski Sürpriz Kutuları'ndan gerçek alım yapabiliyordu → kapandı. Denetçi 19 bağlamdaki bütün düğmeleri taradı: eski mağazaya hiçbir yol kalmadı.
  - **Denetçinin bulgusu:** sandık yuvaları yeni menüde yoktu. Maç galibiyeti ve Bronz Sandık adımından gelen sandıklar açılamıyordu → aynı ekrana **SANDIKLARIM** (4 yuva) eklendi. Hazır sandıklar Hediyeler rozetinde sayılıyor; galibiyet mesajı "Hediyeler → Efsane Sandıklar'dan aç." oldu.
  - Android geri tuşu: menüye döner ve Hediyeler penceresini açar.
- **G-01 — Pot çipi:** maç ekranında üst ortadaki çip yığını Furkan'ın yeni çip görseli (arka plan temizlendi, saydam). Miktar canlı ve odanın ödülüne göre: Portekiz 500 … İstanbul 500M. Turnuva, Şans, Egzersiz, 2 Kişi eskisi gibi (pot göstermiyorlardı).
- **G-02 — Amblem:**
  - Giriş efekti yeni kare amblemle (dönerek gelme, 8 topuna çarpma parlaması, ışık süpürmesi, parıltılar amblemin üstündeki noktalara göre). Süre ve dokununca geçme aynı.
  - Telefon simgesi: köşeleri saydam amblem; uyarlanabilir simgede amblem (54 dp) lacivert degrade zemin üstünde, daire/kare/squircle maskelerinin hiçbirinde çerçeve kesilmiyor.
  - Play Store için `docs/magaza/play_ikon_512.png`.
- Testler: 45 (yeni: Efsane Sandıklar toplama, eski mağaza kapalı, pot görseli/miktarı, simge boyutları).

---

## BÖLÜM 4 — Oyunun içeriği (surum-78 itibarıyla)
- **Ülke masaları (1'e 1):** 17 oda. Ödül = 2 × giriş, net kazanç = giriş. 1'e 1'de ülkenin kendi masası kullanılır.
  - Portekiz 250 · İtalya 1K · Fransa 4K · Hollanda 5K · Brezilya 10K · Japonya 50K · Mısır 100K
  - İspanya 250K · Almanya 500K · İngiltere 1M · Rusya 2,5M · Kore 5M · Amerika 10M
  - Dubai 25M · Monako 50M · Las Vegas 100M · İstanbul 250M
- **OYNA düğmesi:** ücret ≤ bakiyenin %15'i olan en yüksek açık masa.
- **Turnuva:** Giriş 1.000, ödül 7.500, 3 tur.
- **Masalar (13, hepsi şu an bedava / seçilebilir):**
  - Klasik 3: Turnuva (varsayılan), Saray Halısı, Mor Saray
  - Resimli 10: Pembe Saray, Zehir Neon, Buz Kristal, Kızıl Ateş, Zümrüt Saray, Gece Moru, Elektrik Mavi, Kara Altın, Gümüş Saray, Lav Alevi
- **İstakalar:** 84 (hepsi Ejder ölçüsü standardında).
- **Mağaza (yeni, 4 sekme):** Özel Teklifler, Çip Paketleri, Dolar Paketleri (TL ile; yayında Google Play ödemesi gelene kadar kapalı), Sandıklar.
- **Günlük:** Günlük Hediye 10.000 çip · Günlük Sandık 1 Nadir parça + 5.000 çip (günde bir).
- **Sandıklar (Dolar ile):** Arena 20 (2 parça + çip) · Şampiyon 50 (5 parça + tebeşir) · Kralın Hazinesi 120 (10 Efsanevi parça + VIP 7 gün). Tebeşir ve VIP şimdilik sadece kayda yazılıyor, etkisi yok.
- **Eski kutular (kodda duruyor, arayüzden kalktı):** Nadir 5/14 · Destansı 16/44 · Efsanevi 33/89; Özel Teklif (Destansı) 11/31.
- **Lig eşikleri (21 günlük net kazanç):** Novice 0 · Pioneer 30K · Nova 150K · Rogue 300K · Valor 1M · Astra 3M · Zenith 10M · Dominion 30M · Eclipse 100M · Paragon 300M. Dönem sonu ödülü: eşiğin %10'u çip + 1 elmas. İlk dönem 17 Kasım 2026'da başladı.
- **Diller:** 6 (giriş ekranlarında). Oyunun geri kalanı Türkçe.

---

## BÖLÜM 5 — Yaşanan hatalar ve dersler
| Sorun | Sebep | Çözüm / ders |
|---|---|---|
| Kodla çizilen ekranlar beğenilmedi | Görsele birebir değildi | Görseli parçalama yöntemi |
| Ekranlar tam ekran değildi | Sabit oran | `fullFit` / `v6fit` ile germe |
| Para simgeleri taştı | Çizilen simgeler | Furkan'ın kendi para çubuğu görseli |
| İlk açılışta siyah ekran, bozuk/dev oyun ekranı | Büyük ihtimalle WebView grafik belleği doldu | Görseller dosyaya taşındı, bellek boşaltma, `ensureScreen`, `selfHeal`, hata kaydı |
| Çip kesildi, maç açılmadı | Ücret maç kurulmadan alınıyordu | `feeGuard` ile iade |
| Çipler sola uçuyordu | Gizli kapsayıcıyı hedef alıyordu | Görünen sayaca uçuş, sabit katman |
| Mağazada masa adı bozuk | Başka bir `.nm` CSS kuralı | Kural kapsamlandı; yeni ekranlarda `v6` öneki |
| surum-70 notunda "Dubai 25 bin" yazıldı | Yanlış bilgi | Doğrusu 25 milyon |
| Resimli avatarla açılışta betik yarıda kalıyordu | `const` değişkene tanımlanmadan erişim (TDZ) | `window.` üzerinden erişim, açılış çağrıları try/catch |
| Sıfırla / yedekten yükle işe yaramıyordu | Sayfa kapanırken eski kayıt geri yazılıyordu | `_bbaNoSave` |
| Satır içine `//` yorum kodun devamını yuttu | Tek satırlık kodda `//` | Satır ortasında sadece `/* */` |
| Testte maç bazen açılmadı | Zaman hızlandırma feeGuard bekçisini de hızlandırıyordu | ≥5000 ms süreler hızlandırılmıyor |
| Oda maçı testi ara sıra kırmızı | Kayıpta seviye ödülü hesaba katılmamıştı | Üst sınıra `lv*250 + titleReward` |
| Yeni düğmeler mor göründü | Genel `button` CSS'i | `.v6 .v6h` için `!important` sıfırlama |
| Masalar ekranı ilk açılışta boş | `show` kurulumdan önce çağrılıyordu | `openTables6` önce `buildTables` |
| **Mağaza düğmeleri parmakla çalışmıyordu (surum-77)** | Tam ekran görünmez katman dokunuşu yutuyordu; `.click()` testleri bunu göremez | `pointer-events:none`; **ders: düğme testleri gerçek dokunuşla yapılır** (`test_dokunus.py`) |
| Dokunuş testinde yalancı hatalar | Önceki dokunuşun açtığı pencere sonrakini kapatıyordu | Her dokunuştan önce ekranı sıfırla (`bbaBack` döngüsü) |

> Siyah ekran, bozuk ekran ya da çalışmayan düğme olursa: **Ayarlar → Hakkında → 📋 Hata raporunu kopyala**, sohbete yapıştır (ya da ekran görüntüsü). Oyunu silmeden önce yapılmalı.

---

## BÖLÜM 6 — Konuşulan kararlar
- **Teknoloji:** Godot zor bulundu → web oyunu + Capacitor + GitHub bulut derleme (ücretli uygulama yapıcılar yerine).
- **Paket adı:** `com.blackballarena.game` (kalıcı; Play Store'a bununla çıkılacak).
- **1'e 1 masası:** ülke masası kalır; oyuncunun seçtiği masa şimdilik 1'e 1'de kullanılmaz (bilinçli karar).
- **Özel Teklif:** %30 indirim (11/31). Yeni mağazada kaldırıldı.
- **Maliyet konuşması (26 Kasım):** Furkan Play Store, sunucu, reklam, global çıkış ve Hetzner maliyetini sordu; günde 50 bin reklam izlenmesinin TL karşılığı konuşuldu. Play Store geliştirici hesabı tek seferlik 25 dolar. Ayrıntılı rakamlar sohbette verildi; kesin bütçe sunucu kararıyla birlikte netleşecek.
- **Sunucu:** **Hetzner** kullanılacak. Firebase'in (giriş vb.) yeri **sonra konuşulacak**. "Panelix" adlı bir proje yok, notlardan kaldırıldı.
- **Hesaplar:** Şimdilik telefonda; Hetzner gelince sunucuya taşınacak. Google/Facebook/Apple girişi sunucuyla gelecek.

---

## BÖLÜM 7 — Bundan sonra ne yapacağız

**Sıradaki işler (27 Kasım, surum-78'den sonra):**
1. **K-00 Profesyonellik denetimi** (oyun 8 Ball Pool ile ekran ekran karşılaştırılır → ekran görüntülü eksikler listesi → K görevleri).
2. Teknik sıra: **1-10** (bütçe kontrolleri) → **1-04** (metinleri tek yerde topla; bütün oyun 6 dile çevrilebilsin) → **1-05** (CSS'i ayır). Son biten: 1-03 / surum-75.
3. Görseller (Faz G) Furkan gönderince araya alınır. (G-01, G-02, G-03 surum-78'de bitti.)
- Ayrıntı: `GOREV_HARITASI.md` → "Sıradaki görev — NEREDE KALDIK".

### Furkan'dan beklenen cevaplar
- **Hangi düğmeler çalışmadı?** surum-77'yi kurup denesin; çalışmayan varsa ekran adı + düğme adı + Hakkında'daki hata raporu (WebView sürümü önemli).
- **Masalar satılık olsun mu?** Şu an 13 masanın hepsi bedava.
- **İki APK** (test ve yayın) aynı paket adıyla üst üste kuruluyor; ikisini yan yana istiyor mu?
- **Yayın APK'sında** çip sayacına dokununca mağaza açılsın mı?
- **Eski mor ekranlar** (9 ekran) için yeni görsel gönderecek mi?

### Denetçinin eksikler listesi (surum-77 taraması)
- **Sadece "yakında" mesajı veren düğmeler:** VIP, Arkadaşlar, Google/Facebook/Apple girişi, Şifremi Unuttum (e-posta), Lig'deki Arkadaş/Ülke/Dünya sekmeleri, Hesap bağla, yayında TL paketleri. → Sunucu (Hetzner) ve ödeme gelince çalışacak.
- **Aynı yere giden düğmeler:** Lig ve Sezon; Gelişim ve Profil; Mağaza ve Özel Teklif.
- **Adıyla tam uyuşmayan hedefler:** Arkadaşla Oyna → eski "Özel Oyun" ekranı.
- **Eski mor tasarımda kalan ekranlar** (yeni mavi/3B görsellerle uyumsuz): ödül penceresi (showLoot), Günlük Hazine, Çark, Gizemli Kartlar, Görevler, Başarımlar, Gelen Kutusu, Altın Atış, Hediyeler paneli, Profil. Eski mağaza G-03 ile kapandı.
- **Etkisiz ödüller:** VIP ve tebeşir sadece kayda yazılıyor.
- **Dil:** sadece giriş ekranları çevrili (1-04 ile çözülecek).
- **Hesaplar** ayrı kayıt değil (aynı telefonda iki hesap aynı ilerlemeyi görür).
- **Eski WebView riski:** eski ekranlarda (.screen dahil ~45 yer) hâlâ `inset` kullanılıyor; Android WebView < 87'de bozulabilir.
- **780×360 ekranda** Gizemli Kartlar düğmeleri kenara yapışık.

### Denetçi alt ajan
- surum-77 denetimini, 27 Kasım'da G-01/G-02/G-03 hazırlık taramasını ve onaylarını yaptı. **Kapatılmadı**; K-00'da aynı ajan devam edecek. Furkan'a haber vermeden kapatılmaz.

### Büyük plan (ayrıntı `docs/YOL_HARITASI.md`)
- **0.** Kararlar (çoğu verildi) · **G.** Görsel paketi · **K.** Kalite ve profesyonellik
- **1.** Temeli sağlamlaştırma (testler ✅, modüller, deterministik fizik)
- **2.** Giriş ve bulut kayıt (Hetzner; Firebase sonra konuşulacak)
- **3.** Sunucuda ekonomi · **4.** Online 1'e 1 · **5.** Gelir (AdMob, Google Play ödeme)
- **6.** Play Store hazırlığı · **7.** Kapalı test (12 kişi, 14 gün) · **8.** Türkiye'de yumuşak çıkış · **9.** Büyüme / global

### Her sürümde izlenen yol
1. `git pull`; istenen iş yapılır (başka ayar bozulmaz).
2. Testler: eski + yeni testler; düğmeler gerçek dokunuşla; ekran görüntüsüyle kontrol. Büyük işlerde denetçi onayı.
3. Commit → push → CI → `surum-N`.
4. Furkan'a: indirme bağlantısı (test + yayın APK), kısa değişiklik listesi.
5. `PROJE_NOTLARI.md`, `YOL_HARITASI.md` ve `GOREV_HARITASI.md` güncellenir.
