# Lig sistemi — sunucu (Firebase) planı

Şu an lig puanı telefonda tutuluyor (`save.lg`). Sunucu bağlanınca aynı kurallar sunucuya taşınacak.
İstemcide hazır kanca: `window.LeagueBackend.report({id, kind, net, sid})` — her kesinleşmiş maç sonucunda bir kez çağrılır.

## Kurallar (istemcide uygulanan, sunucuya aynen taşınacak)
- Dönem: 21 gün, başlangıç 17 Kasım 2026 00:00 (TR). `sid = floor((now - EPOCH) / 21 gün)`
- Puan = dönem içindeki NET kazanç = ödül − giriş ücreti (bahis kazanç sayılmaz)
- Her maç sonucu benzersiz maç kimliğiyle yalnızca bir kez eklenir
- Eşikler: Novice 0 · Pioneer 30K · Nova 150K · Rogue 300K · Valor 1M · Astra 3M · Zenith 10M · Dominion 30M · Eclipse 100M · Paragon 300M
- Dönem sonu: sonuç `hist`e yazılır, eşiğin %10'u çip + 1 elmas ödül BİR kez verilir, dönem puanı sıfırlanır

## Sunucu tasarımı (Firebase Auth + Firestore + Cloud Functions)
1. `startMatch(roomId)` (callable): oyuncunun bakiyesinden giriş ücretini düşer, `matches/{id}` = {uid, roomId, fee, prize, status:'live', t}
2. `finishMatch(id, result)` (callable): transaction içinde status 'live' ise → 'done'; kazandıysa bakiye += prize ve
   `leagues/{sid}/players/{uid}.pts += prize − fee`. Status zaten 'done' ise hiçbir şey yapılmaz (çift ekleme yok)
3. Zamanlanmış fonksiyon (her saat): biten dönemlerin oyuncularına ödülü `rewardPaid` bayrağıyla bir kez yazar, sonucu `seasons/{sid}` altında saklar
4. Firestore kuralları: istemci bakiye / puan alanlarına yazamaz; sadece fonksiyonlar yazar
5. Zaman her zaman sunucu saatinden alınır (telefon saati değiştirilerek dönem atlatılamaz)

Gerekenler: Firebase projesi (Cloud Functions için Blaze planı), Android uygulama kaydı + google-services.json,
GitHub Actions için dağıtım anahtarı (FIREBASE_TOKEN / servis hesabı) — bunlar gelince fonksiyonlar yazılıp CI ile dağıtılır.
