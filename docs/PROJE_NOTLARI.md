# Blackball Arena — Proje Not Defteri

Yeni bir sohbette her şeyi baştan anlatmamak için tutulur.
Yeni sohbette ilk mesaj: **"docs/PROJE_NOTLARI.md dosyasını oku, oradan devam et."**

Son güncelleme: 25 Kasım 2026 · Son sürüm: **surum-77**

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
| APK indirme | `…/releases/download/surum-N/BilardoUstasi.apk` (test modu açık) · `…/BlackballArena-yayin.apk` (test modu kapalı, ayrı kayıt) |
| Paket adı | **`com.blackballarena.game`** (kalıcı ad, surum-72'den itibaren; eskisi `com.bilardoustasi.oyun`) |
| Tasarım dili | Siyah + altın; mor vurgular; turnuva mavisi varsayılan masa |
| Para birimleri | **Çip** (siyah-altın taçlı "B" çip görseli), **Nakit** (yeşil banknot destesi), **Elmas** |

### Furkan'ın kalıcı kuralları
1. **"Bekle / başlama / not al"** → sadece not alınır. **"Başla" / "yap"** → uygulanır.
2. **Başka hiçbir şeyin ayarı bozulmaz.** Sadece istenen değişir.
3. **Ekranlar Furkan'ın görsellerine birebir yapılır:** Görsel parçalanır, yazılar silinip canlı yazı konur. Ekranlar tam ekran olur ve butonlar çalışır. Kodla çizilmiş taklit "acemice" bulundu, istenmiyor.
4. Masa görselleri toplu gelir, "yap" denince soru sormadan her biri ayrı tema olarak eklenir.
5. Gerçek kişi benzerliği ve telifli karakter (Naruto, Goku vb.) yapılmaz.
6. Yeni APK kurmadan önce eskisi silinmeli (şu an test imzası kullanılıyor).
7. Test parası, kilit açmalar ve kısayollar tek bayrağa bağlı (`window.BBA_DEV`); yayın APK'sında kapalı. İsim TÜRKPATENT/WIPO'da kontrol edilecek.
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
  - İki yuva: `KEY` (ana) ve `KEY_B` (bir adım geride yedek); bozuk ana kayıt `KEY_X`'te saklanır. `validSave`, `saveRepair`, `bbaTrim` (sınırlar `BBA_LIM`).
  - Sıfırla/yedekten yükle `window._bbaNoSave=1` ile sayfa kapanırken eski kaydın geri yazılmasını engeller.
- **Teşhis:** `bbaLog` (son 50 hata), `bbaIz` (açılış izi; önceki açılış `bba_iz_onceki`), `bbaReport()` → Ayarlar → Hakkında'dan kopyala/paylaş. `BBA_SURUM` CI'da yazılır.
- **Telefon köprüsü:** `native/MainActivity.java` içinde `BbaNative` Capacitor eklentisi (`saveText`, `shareText`); JS'te `bbaNat()`, `bbaSaveFile()`, `bbaShare()`.
- **Testler:** `tests/` (pytest + Playwright, 35 test). CI'da `test` işi geçmezse APK derlenmez. Yeni düzeltilen her hataya bir test eklenir.
  - Görünüş testi (`test_gorunus.py`): 23 ekran önceki commit'le karşılaştırılır. Bilerek görünüş değiştiren commit mesajına **`[görünüş]`** yazılır.
- **Test modu:** `window.BBA_DEV=true;/*DEV*/` (kaynakta açık). CI yayın APK'sında `false` yazar. Yayın sürümünün kayıt anahtarı `bilardo_ustasi_v1_yayin`.
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

### 25 Kasım — surum-72
- **Kararlar:** 1'e 1'de ülke masası kalır (seçilen masa 1'e 1'e uygulanmaz). Özel Teklif %30 indirimli. Kalıcı paket adı `com.blackballarena.game`.
- **Özel Teklif fiyatı:** Destansı Kutu 1 tane **11**, 3 tane **31** nakit (`OFFER_PRICE`, `buyOffer`). Sürpriz Kutuları'ndaki normal fiyat 16/44 aynı kaldı. Şimdilik günlük sınır yok.
- **Paket adı değişti:** `capacitor.config.json`, `native/MainActivity.java`, `build.yml`. Yeni APK eski uygulamanın yanına ayrı uygulama olarak kurulur; eski "Blackball Arena" silinmeli.

### 25 Kasım — surum-73 (hata avı: 22 düzeltme)
Kod baştan tarandı. Bir denetçi alt ajan bağımsız tarama yaptı ve her düzeltmeyi ayrıca test edip onayladı. Testler tarayıcıda yapıldı (Playwright + Chrome); 2 kişilik kural simülasyonunda binlerce atış ve fizik fuzz testi çalıştırıldı.
- **Kritik**
  - Pes et/ayrıl sırasında yuvarlanan 8 → maç hem kayıp hem galibiyet sayılıyor, ödül veriliyordu. Çözüm: `goDone` bayrağı (gameOver maç başına bir kez) ve `endShot` başında `if(over)return`.
  - Resimli avatar seçen oyuncuda her açılışta `AV_ART` TDZ hatası oluyordu. Büyük betiğin kalanı çalışmıyordu: `fullFit`, lifecycle (30 sn) ve antiCheat devre dışıydı. Siyah/bozuk ekran şikâyetiyle ilgili olabilir. Çözüm: `myAvT` artık `window.AV_ART` kullanıyor, açılış çağrısı try/catch içinde.
  - Ayarlar → "İlerlemeyi sıfırla" ve "Yedekten geri yükle" hiç çalışmıyordu: sayfa kapanırken `persist()` eski kaydı geri yazıyordu. Çözüm: `window._bbaNoSave` bayrağı.
- **Para / ödül**
  - Sürpriz Kutusu efekti sürerken ikinci basışta nakit iki kez düşüyordu. Çözüm: `_boxLock`.
  - Gizemli Kart kazınmadan kapatılırsa ödül kayboluyordu; çark dönerken oyun kapanırsa ödül gidiyordu. Çözüm: ödül `save.pendRw` olarak hemen kayda geçiyor, kapatınca veriliyor, yarım kalırsa açılışta gelen kutusuna not düşülerek veriliyor.
  - Ücret zaman aşımıyla iade edildikten sonra eşleşme yine maç açabiliyordu (bedava maç). Çözüm: `_feeVoid`.
  - 9 Top / Kılavuzsuz odalarında 20. galibiyet yanlışlıkla İtalya/Fransa istakası veriyordu. Artık sadece ülke odaları rozet veriyor.
  - Gelen kutusu 20 mesajı aşınca alınmamış ödülleri siliyordu. Artık ödüllüler korunuyor.
- **Güvenlik**
  - Oyuncu adındaki HTML kodu çalışıyordu. Çözüm: `cleanName` (< > & " ' ` \ temizlenir, en fazla 14 karakter).
  - Yedek kodundan gelen avatar, ID ve gelen kutusu alanları yüklemede temizleniyor.
- **Küçükler**
  - Turnuva eşleşme ekranı giriş ücretini 3.750 gösteriyordu (doğrusu 1.000); 2. ve 3. turda artık sadece ödül görünüyor.
  - Kutu ödül penceresi başka pencereyle ezilince çıkan hata giderildi.
  - "Kopyalandı" mesajı artık kopyalama başarısızsa çıkmıyor (`bbaCopy`: yedek kodu, ID, profil).
  - Altın Atış sonucunda Android geri tuşu menüye götürüyor; cep bilgisi yoksa NaN koruması var.
  - Yapay zekâ hedef bulamazsa çökmüyor.
  - Görev metni "Bursa" yerine "İtalya veya üstü".
  - Menüdeki sandık yuvaları artık her saniye değil, sadece yazı değişince yeniden çiziliyor.
  - 780 px ekranda ıstaka etiketi ("İMPARATOR") kesilmiyor.
  - Kayıtta artık olmayan ıstaka/masa seçiliyse açılışta Başlangıç ıstakası / Turnuva masasına dönülüyor.
- **Bilerek bırakılanlar**
  - `openGifts` iki kez tanımlı (ölü kod, zararsız).
  - Lig puanı sadece kazançla artıyor (kayıp düşmüyor), tasarım kararı.
  - Yedek kodu ile bakiye değiştirilebiliyor; sunucu ekonomisi (ADIM 3) gelince çözülecek.

### 26 Kasım — surum-77 (acil: mağaza düğmeleri)
- Furkan: "çoğu buton çalışmıyor". Sebep: mağazada tam ekran görünmez bir katman Geri, sekmeler ve "+" düğmelerinin üstündeydi. `.click()` ile yapılan testler bunu yakalayamadı. Düzeltildi (`pointer-events:none`).
- Yeni kalıcı test `tests/test_dokunus.py`: yeni ekranlardaki 100'den fazla düğmenin her birine gerçek parmak dokunuşu yapılıyor. Eski sürümde bu test kırmızı veriyor.
- Denetçinin listesi (`eksikler`): dokunuşu engelleyen başka bir şey yok. "Çalışmıyor gibi görünenler": sadece "yakında" mesajı veren düğmeler (VIP, Arkadaşlar, sosyal girişler, Lig'deki Arkadaş/Ülke/Dünya sekmeleri), aynı yere giden düğmeler, eski mor tasarımda kalan 9 ekran, etkisiz VIP/tebeşir. Bunlar Furkan'a soruldu.

### 26 Kasım — surum-76 (Furkan'ın 12 yeni görseli: giriş, menü, mağaza, masalar)
- Bütün ekranlar Furkan'ın görsellerinden parçalandı (yazılar silindi, değişen yazılar canlı). Tasarım ölçüsü 1600×900; `.v6` katmanı, `v6fit()` ile tam ekrana yayılıyor. Kod: index.html sonunda `/* ===== V6 */` bloğu. Eski ekranlar silinmedi; yeni katman üstte, eski düğmelerin işlevleri çağrılıyor.
- **Giriş:** Giriş Yap / Üye Ol / Misafir / Google-Facebook-Apple (sunucu gelince) / ses / dil.
  - Pencereler: Giriş Yap (hata hâli ayrı görsel), Şifremi Unuttum, Üye Ol, Dil Seçimi.
  - **Hesaplar şimdilik telefonda** (`bba_acc`, şifre PBKDF2 ile, açık saklanmaz). Hetzner gelince sunucuya taşınacak.
  - **6 dil** (tr, en, es, de, fr, ar; Arapça sağdan sola): giriş ekranları çevrili, oyunun geri kalanı 1-04 ile çevrilecek.
- **Ana menü (mavi):**
  - Canlı: isim, seviye, XP çubuğu, para, avatar (seçildiyse), posta ve ıstaka rozetleri, Sezon, Günlük Sandık ve Özel Teklif süreleri.
  - OYNA: giriş ücreti bakiyenin en fazla %15'i olan en yüksek açık ülke masası (birikim tek dokunuşta gitmesin). Dünya Çapında Oyna: ülke listesi. Arkadaşla Oyna: Özel Oyun. Gelişim: Profil.
- **Mağaza (4 sekme):** Özel Teklifler, Çip Paketleri, Dolar Paketleri, Sandıklar (fiyatlar görseldeki gibi).
  - TL paketleri: test APK'sında onayla bedava, yayında "ödeme Google Play sürümünde".
  - Günlük Hediye (10.000 çip) ve Günlük Sandık (1 Nadir parça + 5.000 çip): günde bir, reklam (AdMob) gelene kadar reklamsız.
  - Sandıklar Dolar ile: Arena 20 (2 parça + çip), Şampiyon 50 (5 parça + tebeşir), Kralın Hazinesi 120 (10 Efsanevi parça + VIP 7 gün). Tebeşir ve VIP şimdilik sadece kayda yazılıyor; etkileri sonra.
  - Eski Sürpriz Kutuları ve Destansı Özel Teklif (11/31) arayüzden kalktı. Hediyeler → Efsane Sandıklar eski ücretsiz ödül listesini açıyor.
- **Masalar ekranı:** Büyük 3B önizleme ve kart sırası. Mevcut 13 masanın hepsi, isimleriyle.
  - Her masanın üst yüzeyi görseldeki 3B masa gövdesine perspektifle oturtuluyor (`homog` → CSS `matrix3d`). Yeni masa eklenince otomatik 3B olur.
  - Karta dokun: önizle. KULLAN: seç.
- Testler: `tests/test_v6.py` eklendi, sandık testi yeniden yazıldı, görünüş testine yeni ekranlar eklendi.

### 26 Kasım — surum-75 (1-02, 1-03, H-05)
- **1-03 / H-05:** Test modu tek bayrak: `BBA_DEV`. Bağlı olanlar: test parası (5B + 10B), `TEST_UNLOCK` (masa kilitleri, bütün ıstaka/masa açma), menü sayacına 5 dokunuş kısayolu. Hakkında ve raporda "TEST MODU" yazar. CI iki APK verir: **BilardoUstasi.apk** (test) ve **BlackballArena-yayin.apk** (gerçek oyuncu hâli: 1.000 çip, kilitli masalar, ayrı kayıt).
- **1-02:** Görünüş testi: 23 ekran önceki commit'le piksel piksel karşılaştırılıyor (gürültü 0, eşik 25 piksel).
- Ayarlar → Güvenlik: "Dosyaya yedek" etiketi düğmeye değmiyor. Telefonun sistem yazı boyutu artık oyunun ekranlarını bozmuyor (`setTextZoom(100)`).

### 26 Kasım — surum-74 (görev haritası: güvenlik ağı)
- **H-01/H-02 (0-01):** Çift yuvalı, doğrulamalı kayıt; bozuk kayıtta yedekten açılış + "Kayıt kurtarıldı" notu; hafıza dolu olunca temizleyip tekrar deneme, olmazsa uyarı; NaN gibi bozuk değerler onarılır. Yedek kodu da `validSave`'den geçer.
- **H-03:** Bütün listeler için tek üst sınır kuralı (`BBA_LIM`, `bbaTrim`).
- **H-08:** Liderlik efekti çizim alanı ekrandan çıkınca boşaltılıyor (~4 MB).
- **0-02 + H-04:** Ayarlar → Hakkında → 📋 Hata raporunu kopyala / 📤 Paylaş. Rapor: sürüm, cihaz (Android, model, WebView, bellek), bu ve önceki açılışın adım adım izi, 3./10. saniyede ekran durumu, son 50 hata. Oyuncu adı ve bakiye raporda yok.
- **0-03:** Ayarlar → Güvenlik → 💾 Kaydet (İndirilenler/BlackballArena/…txt), 📂 Dosyadan yükle (aynı doğrulama ve çift onay), 📤 Paylaş (Drive/WhatsApp).
- **0-04:** `docs/CIHAZ_TEST_LISTESI.md` (15 madde, 5 dakika).
- **1-01:** `tests/` klasörü, 32 otomatik test; GitHub'da APK'dan önce çalışır.
- Denetçi alt ajan her görevi ayrıca test etti; bulduğu 5 uyarı (NaN'da kaydın durması, geçersiz yedek kodu, iz gürültüsü, telefonda sahte "kaydedildi" mesajı, Capacitor eklenti erişimi) düzeltildi.

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
- **Kutular (1 tane / 3 tane, nakit):** Nadir 5/14 · Destansı 16/44 · Efsanevi 33/89. Özel Teklif (Destansı): 11/31.
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
| Resimli avatarla açılışta betik yarıda kalıyordu | `const` değişkene tanımlanmadan erişim (TDZ) | `window.` üzerinden erişim, açılış çağrıları try/catch |
| Sıfırla / yedekten yükle işe yaramıyordu | Sayfa kapanırken eski kayıt geri yazılıyordu | `_bbaNoSave` bayrağı |
| Satır içine `//` yorum eklemek kodun devamını yuttu (surum-73 sırasında yakalandı) | Tek satırlık kodda `//` | Satır ortasında sadece `/* */` kullan |
| Testte zamanlayıcıları 20 kat hızlandırınca maç bazen açılmadı | feeGuard'ın 16 sn bekçisi de hızlandı | Testlerde en fazla 4 kat hızlandır |

> Siyah ekran ya da bozuk ekran tekrar olursa: **oyunu silmeden önce Ayarlar → Hakkında'daki "Hata kaydı"nın fotoğrafı çekilip gönderilsin.**

---

## BÖLÜM 4 — Bundan sonra ne yapacağız
Ayrıntılı, adım adım plan ve durum takibi **`docs/YOL_HARITASI.md`** defterindedir. Tek kaynak orasıdır; plan değişince orası güncellenir.
Oturum oturum somut görevler (bilinen hatalar dahil): **`docs/GOREV_HARITASI.md`**.

**⏸ BEKLEMEDE (26 Kasım 07:36) — Furkan "bekle, başlama" dedi.**
- Karar: Görev haritasına **AŞAMA K (Kalite ve profesyonellik)** eklendi. Furkan "başla" deyince ilk iş **K-00 Profesyonellik denetimi**: oyun 8 Ball Pool ile ekran ekran karşılaştırılacak, ekran görüntülü eksikler listesi çıkacak, eksikler K görevleri olarak haritaya girecek.
- Teknik sırada kalınan yer: 1-10 → 1-04 → 1-05 (son biten 1-03 / surum-75).
- Ayrıntı: `GOREV_HARITASI.md` → "Sıradaki görev — NEREDE KALDIK".
- Görseller (Faz G) Furkan gönderince araya alınır.

Kısaca sıra:
- **0.** Kararlar (çoğu verildi)
- **G.** Görsel paketi
- **1.** Temeli sağlamlaştırma (testler depoya, modüller, deterministik fizik)
- **2.** Firebase giriş ve bulut kayıt
- **3.** Sunucuda ekonomi
- **4.** Online 1'e 1
- **5.** Gelir
- **6.** Play Store hazırlığı
- **7.** Kapalı test (12 kişi, 14 gün)
- **8.** Türkiye'de yumuşak çıkış
- **9.** Büyüme

### Her sürümde izlenen yol
1. İstenen iş yapılır (başka ayar bozulmaz).
2. Testler: tüm eski testler ve yeni testler (ekran görüntüsüyle kontrol).
3. Commit → push → CI → `surum-N`.
4. Furkan'a: indirme bağlantısı, ekran görüntüsü, kısa değişiklik listesi.
5. `PROJE_NOTLARI.md` ve `YOL_HARITASI.md` güncellenir.
