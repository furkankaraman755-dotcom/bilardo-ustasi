"""0-02 / H-04 / H-08: hata raporu, açılış izi, kopyalama, liderlik belleği."""
from conftest import no_errors

CLIP_OK = "Object.defineProperty(navigator,'clipboard',{value:{writeText:t=>{window._cb=t;return Promise.resolve()}}})"
CLIP_NO = "Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('deny'))}});document.execCommand=()=>false"

def test_hata_raporu(game):
    g = game(init=CLIP_OK); g.login()
    g.js("bbaLog(new Error('deneme hatası'),'test')"); g.reload()
    g.js("openSettings();stTab='hak';stRender()"); g.wait(200)
    g.js("document.getElementById('stRap').click()"); g.wait(300)
    t = g.js("window._cb||''")
    for part in ('HATA RAPORU', 'CİHAZ:', 'ÖNCEKİ AÇILIŞ İZİ', 'BU AÇILIŞ İZİ', 'kayıt yüklendi', 'deneme hatası', 'surum-'):
        assert part in t, part
    assert 'Test' not in t, 'raporda oyuncu adı olmamalı'

def test_iz_tekrarlari_yazmaz_ilk_satirlar_korunur(game):
    g = game()
    ek = "BBA_IZ.filter(x=>x[1].startsWith('ekran:')).length"
    n0 = g.js(ek)
    for _ in range(3):
        g.js("dispatchEvent(new Event('focus'));dispatchEvent(new Event('pageshow'))"); g.wait(700)
    assert g.js(ek) == n0, 'öne gelişte aynı ekran ize tekrar yazıldı'
    g.js("for(let i=0;i<100;i++)bbaIz('x'+i)")
    assert g.js("BBA_IZ[0][1]").startswith('betik başladı') and g.js("BBA_IZ.length") == 60

def test_kopyalama_izin_yoksa_yalan_soylemez(game):
    g = game(init=CLIP_NO); g.login()
    out = []
    for tab, btn in (('guv', 'stBak'), ('hes', 'stCopy')):
        g.js(f"openSettings();stTab='{tab}';stRender()"); g.wait(200)
        g.js(f"document.getElementById('{btn}').click()"); g.wait(300)
        out.append(g.js("document.getElementById('stM').textContent"))
    assert all('Kopyalanamadı' in x for x in out), out
    no_errors(g)

def test_liderlik_cizim_alani_bosaltilir(game):
    g = game(); g.login()
    g.js("openLead()"); g.wait(1200)
    assert g.js("document.getElementById('ldFx').width") > 2
    g.js("leadGoBack()"); g.wait(300)
    assert g.js("document.getElementById('ldFx').width*document.getElementById('ldFx').height") <= 1
