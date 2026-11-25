# Claude için

Bu proje Blackball Arena mobil bilardo oyunudur. İşe başlamadan önce **docs/PROJE_NOTLARI.md** dosyasını oku:
proje özeti, kullanıcının kuralları, kod yapısı, sürüm geçmişi ve yaşanan hatalar oradadır.
Sıradaki işler ve durum takibi için **docs/YOL_HARITASI.md** defterini oku; hangi fazda olduğumuz orada yazar.

Kısa kurallar:
- Kullanıcıyla Türkçe konuş. Kullanıcı sadece telefondan çalışıyor.
- "Bekle / başlama / not al" → sadece not al. "Başla" → uygula.
- Başka hiçbir özelliğin ayarını bozma. Yeni özellikleri mümkünse sona eklenen betiklerle (sarmalayarak) ekle.
- Ekranlar kullanıcının görsellerinden parçalanarak, tam ekran yapılır.
- Görseller `a/` klasörüne dosya olarak konur (HTML'e base64 gömülmez).
- Her işten sonra: test et → commit → push → CI (`surum-N`) → indirme bağlantısını ver.
- Her sürümden sonra docs/PROJE_NOTLARI.md ve docs/YOL_HARITASI.md güncellenir.
- Başka bir sohbet de bu depoda çalışıyor olabilir: işe başlamadan önce `git pull` yap.
