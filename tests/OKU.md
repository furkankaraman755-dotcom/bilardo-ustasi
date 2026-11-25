# Otomatik testler (GOREV_HARITASI 1-01)

- Her `git push`'ta GitHub'da önce bu testler çalışır. **Biri bile kırmızıysa APK derlenmez ve yayınlanmaz.**
- Testler oyunu gerçek bir tarayıcıda (Chromium) açar, ekranlara dokunur, maç oynatır ve sonuçları kontrol eder.
- Yerelde çalıştırmak için: `pip install pytest playwright && python -m playwright install chromium && python -m pytest -q tests`
  (Chrome yolu vermek için: `BBA_CHROME=/usr/bin/google-chrome`).

| Dosya | Neyi korur |
|---|---|
| `test_acilis.py` | Açılış hatasız mı, bütün ekranlar açılıyor mu, farklı kayıt durumlarında açılış |
| `test_kurallar.py` | 8/9 top simülasyonu (fizik ve kurallar), pes etmede tek sonuç, yapay zekâ |
| `test_ekonomi.py` | Maç ücreti/ödülü, turnuva, kutu çift basış, Özel Teklif fiyatı, iade, rozet |
| `test_oduller.py` | Çark, kart, kutu penceresi, gelen kutusu sınırları |
| `test_kayit.py` | Çift yuvalı kayıt, bozuk kayıt, hafıza dolu, sıfırla, yedek kodu, dosya yedeği |
| `test_guvenlik.py` | İsim ve yedek kodu ile kod çalıştırılamaması |
| `test_rapor.py` | Hata raporu, açılış izi, kopyalama, liderlik belleği |

Yeni bir hata düzeltildiğinde, o hatanın geri gelmesini önleyen bir test buraya eklenir.
