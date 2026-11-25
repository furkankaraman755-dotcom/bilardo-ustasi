# Claude için

Bu proje Blackball Arena mobil bilardo oyunudur. İşe başlamadan önce **docs/PROJE_NOTLARI.md** dosyasını oku:
proje özeti, kullanıcının kuralları, kod yapısı, sürüm geçmişi, yaşanan hatalar ve bekleyen işler oradadır.

Kısa kurallar:
- Kullanıcıyla Türkçe konuş. Kullanıcı sadece telefondan çalışıyor.
- "Bekle / başlama / not al" → sadece not al. "Başla" → uygula.
- Başka hiçbir özelliğin ayarını bozma. Yeni özellikleri mümkünse sona eklenen betiklerle (sarmalayarak) ekle.
- Ekranlar kullanıcının görsellerinden parçalanarak, tam ekran yapılır.
- Görseller `a/` klasörüne dosya olarak konur (HTML'e base64 gömülmez).
- Her işten sonra: test et → commit → push → CI (`surum-N`) → indirme bağlantısını ver.
- Her sürümden sonra docs/PROJE_NOTLARI.md güncellenir.
