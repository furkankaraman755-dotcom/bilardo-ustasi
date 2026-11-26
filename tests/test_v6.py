"""surum-76: Furkan'ın görselleriyle yeni giriş, pencereler, dil, ana menü, mağaza ve masalar."""
from conftest import no_errors

def ui(g, sel):  # görünür bir düğmeye aria-label ile tıkla
    g.js(f"""(()=>{{const b=[...document.querySelectorAll('.v6h')].filter(x=>x.getAttribute('aria-label')=={sel!r}&&x.offsetParent);if(!b.length)throw new Error('yok: '+{sel!r});b[b.length-1].click();}})()""")
    g.wait(150)

def test_uye_ol_ve_giris(game):
    g = game()
    g.js("localStorage.removeItem('bba_acc');save.pid=0;save.name='';persist();show('login')"); g.wait(200)
    ui(g, 'ÜYE OL')
    g.js("v6n.value='Ali';v6e2.value='ali@ornek.com';v6p1.value='123456';v6p2.value='123456'")
    ui(g, 'HESAP OLUŞTUR')  # koşullar onaylanmadı
    assert 'koşulları' in g.js("document.querySelector('.v6msg').textContent")
    ui(g, 'Seç'); ui(g, 'HESAP OLUŞTUR'); g.wait(600)
    assert g.js("[document.querySelector('.screen.show').id,save.name,save.pid>0,save.email]")[:3] == ['menu', 'Ali', True]
    acc = g.js("JSON.parse(localStorage.getItem('bba_acc'))")
    assert len(acc) == 1 and '123456' not in str(acc), 'şifre açık saklanmamalı'
    # yanlış şifre → hata ekranı; doğru şifre → menü
    g.js("show('login')"); ui(g, 'GİRİŞ YAP')
    g.js("v6u.value='ali';v6p.value='yanlis1'"); ui(g, 'GİRİŞ YAP'); g.wait(600)
    assert g.js("document.querySelector('.v6m img').src").endswith(g.js("'32cdfcdfc0ba.webp'")) or 'Hatalı' in g.js("document.querySelector('.v6m').textContent")
    g.js("v6u.value='ali@ornek.com';v6p.value='123456'"); ui(g, 'GİRİŞ YAP'); g.wait(600)
    assert g.js("document.querySelector('.screen.show').id") == 'menu'
    no_errors(g)

def test_misafir_ve_dil(game):
    g = game()
    g.js("save.pid=0;save.name='';persist();show('login')"); g.wait(200)
    ui(g, 'Dil'); ui(g, 'en'); ui(g, 'ONAYLA'); g.wait(200)
    assert 'LOG IN' in g.js("document.querySelector('#login .v6').textContent")
    ui(g, 'Dil'); ui(g, 'ar'); ui(g, 'CONFIRM'); g.wait(200)
    assert g.js("document.querySelector('#login .v6').getAttribute('dir')") == 'rtl'
    ui(g, 'Dil'); ui(g, 'tr'); ui(g, 'تأكيد'); g.wait(200)
    ui(g, 'MİSAFİR OLARAK OYNA'); g.wait(300)
    assert g.js("[document.querySelector('.screen.show').id,/^Misafir\\d{4}$/.test(save.name)]") == ['menu', True]
    no_errors(g)

def test_ana_menu_dugmeleri(game):
    g = game(); g.login()
    g.js("show('menu')"); g.wait(300)
    assert g.js("document.querySelector('#menu .v6').textContent").count('Test') >= 1
    for lab, scr in [('Masalar', 'tbl6'), ('Mağaza', 'shop6'), ('Dünya Çapında Oyna', 'rooms'), ('Turnuva', 'events'), ('Arkadaşla Oyna', 'priv')]:
        g.js("show('menu')"); g.wait(150); ui(g, lab); g.wait(250)
        assert g.js("document.querySelector('.screen.show').id") == scr, lab
    g.js("show('menu')"); ui(g, 'İstakalar'); g.wait(300)
    assert g.js("document.querySelector('.screen.show').id") == 'cues'
    g.js("show('menu')"); ui(g, 'Ayarlar'); g.wait(300)
    assert g.js("!!document.querySelector('.st4')")
    no_errors(g)

def test_masalar_secimi(game):
    g = game(); g.login()
    g.js("openTables6()"); g.wait(500)
    n = g.js("document.querySelectorAll('#tbl6 .v6C').length")
    assert n == g.js("TABLES.length")
    g.js("[...document.querySelectorAll('#tbl6 .v6C')].find(c=>c.dataset.id==='t_lav').click()"); g.wait(200)
    assert 'LAV' in g.js("document.querySelector('#tbl6 .v6').textContent")
    assert g.js("save.table") != 't_lav'   # önizleme seçmez
    g.js("[...document.querySelectorAll('#tbl6 .v6C')].find(c=>c.dataset.id==='t_lav').querySelector('.v6pl').click()"); g.wait(200)
    assert g.js("save.table") == 't_lav'
    assert g.js("document.querySelectorAll('#tbl6 .v6Top').length") == n + 1
    no_errors(g)

def test_gunluk_hediye_ve_sandik(game):
    g = game(); g.login()
    g.js("openShop6('ozel')"); c0 = g.js("save.coins")
    g.js("V6API.claimGift()"); g.wait(1500); g.js("closeDlg()")
    assert g.js("save.coins") - c0 == 10000
    c1 = g.js("save.coins"); g.js("V6API.claimGift()"); g.wait(300)
    assert g.js("save.coins") == c1, 'günlük hediye iki kez alındı'
    g.js("openDailyChest()"); g.wait(1500); g.js("closeDlg()")
    assert g.js("save.g6.chest>0")
    no_errors(g)
