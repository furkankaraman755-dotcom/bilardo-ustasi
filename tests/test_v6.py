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


def test_pot_cipi_yeni_gorsel_ve_bahse_gore_miktar(game):
    """surum-78 (G-01): maç ekranında pot kutusu Furkan'ın yeni çip görseli; miktar odanın ödülü."""
    g = game(fast=0.25); g.login()
    g.js("startRoom(ROOMS[16])"); g.page.wait_for_function("document.querySelector('#stake .hpile')", timeout=20000)
    assert 'ab5caad93a35' in g.js("getComputedStyle(document.querySelector('#stake .hpile')).backgroundImage")
    assert g.js("document.querySelector('#stake .hpv').textContent") == g.js("fmt(ROOMS[16].prize)") == '500M'
    no_errors(g)

def test_amblem_giris_efekti_ve_simgeler():
    """surum-78 (G-02): giriş efekti yeni amblemi kullanır; Android simgeleri doğru boyutta ve saydam."""
    import pathlib
    from PIL import Image
    root = pathlib.Path(__file__).resolve().parent.parent
    html = (root / 'index.html').read_text(encoding='utf-8')
    assert 'id="inImg" alt="" decoding="async" src="a/31f842b3c833.webp"' in html
    assert (root / 'a' / '31f842b3c833.webp').exists()
    for k, f in {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}.items():
        d = root / 'native' / 'res' / f'mipmap-{k}'
        for n, dp in [('ic_launcher', 48), ('ic_launcher_round', 48), ('ic_launcher_foreground', 108), ('ic_launcher_background', 108)]:
            im = Image.open(d / f'{n}.png')
            assert im.size == (round(dp * f),) * 2, (k, n, im.size)
        fg = Image.open(d / 'ic_launcher_foreground.png')
        assert fg.mode == 'RGBA' and fg.getpixel((0, 0))[3] == 0  # köşeler saydam (maskede kesilmesin)
    for x in ['ic_launcher.xml', 'ic_launcher_round.xml']:
        assert '@mipmap/ic_launcher_background' in (root / 'native/res/mipmap-anydpi-v26' / x).read_text()
