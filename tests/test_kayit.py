"""H-01/H-02/0-03: çift yuvalı kayıt, hafıza dolu, sıfırla, yedek kodu ve dosya yedeği."""
import base64, json, pathlib
from conftest import no_errors

def test_yedek_yuva_bir_adim_geride(game):
    g = game(); g.login()
    g.js("save.coins=1000;persist();save.coins=2000;persist()")
    assert g.js("[JSON.parse(localStorage.getItem(KEY)).coins,JSON.parse(localStorage.getItem(KEY_B)).coins]") == [2000, 1000]

def test_bozuk_ana_kayit_yedekten_acilir(game):
    g = game(); g.login('Ali')
    g.js("save.coins=1000;persist();save.coins=2000;persist();const r=localStorage.getItem(KEY);localStorage.setItem(KEY,r.slice(0,r.length/2))")
    g.reload()
    assert g.js("[save.name,save.coins,_saveInfo.src,!!localStorage.getItem(KEY_X)]") == ['Ali', 1000, 'yedek', True]
    assert g.js("save.inbox[0].t") == 'Kayıt kurtarıldı'
    assert g.js("document.querySelector('.screen.show').id") == 'menu'
    no_errors(g)

def test_iki_yuva_bozuksa_giris_ekrani(game):
    g = game(); g.login()
    g.js("localStorage.setItem(KEY,'{bozuk');localStorage.setItem(KEY_B,'xx')"); g.reload()
    assert g.js("[_saveInfo.src,document.querySelector('.screen.show').id,localStorage.getItem(KEY_X)]") == ['yeni', 'login', '{bozuk']

def test_hafiza_dolu(game):
    g = game(); g.login()
    g.js("""window._mode=1;const O=Storage.prototype.setItem;Storage.prototype._o=O;
      Storage.prototype.setItem=function(k,v){const full=window._mode===2||(window._mode===1&&(this.getItem(KEY_X)!==null||this.getItem(KEY_B)!==null));
        if((k===KEY||k===KEY_B)&&full){const e=new Error('dolu');e.name='QuotaExceededError';throw e;}return Storage.prototype._o.call(this,k,v)};
      localStorage.setItem(KEY_X,'x')""")
    # gereksizler temizlenince kayıt yazılabiliyor
    assert g.js("save.coins=5555;[persist(),JSON.parse(localStorage.getItem(KEY)).coins]") == [True, 5555]
    # hiç yer yoksa: oyun çökmüyor, oyuncu bir kez uyarılıyor
    g.js("window._mode=2")
    assert g.js("[persist(),[...document.querySelectorAll('div')].some(d=>/hafızası dolu/.test(d.textContent))]") == [False, True]
    g.js("window._mode=0")
    assert g.js("persist()") is True

def test_nan_onarilir_kayit_durmaz(game):
    g = game(); g.login()
    r = g.js("()=>{save.gems=12;persist();save.coins=NaN;for(let i=0;i<20;i++)persist();save.gems+=5;const ok=persist();const k=JSON.parse(localStorage.getItem(KEY));return [ok,k.gems,Number.isFinite(k.coins)]}")
    assert r == [True, 17, True]

def test_sifirla(game):
    g = game(); g.login('Ali')
    g.js("persist();persist();openSettings();stTab='guv';stRender()"); g.wait(200)
    g.js("document.getElementById('stRst').click();document.getElementById('stRst').click()")
    g.page.wait_for_load_state('load'); g.page.wait_for_function("typeof save==='object'&&!!window.bbaReport"); g.wait(1500)
    assert g.js("[save.name,document.querySelector('.screen.show').id]") == ['', 'login']

def test_yedek_kodu_gecerli_ve_gecersiz(game):
    g = game(); g.login('Eski')
    g.js("openSettings();stTab='guv';stRender()"); g.wait(200)
    bad = base64.b64encode(json.dumps({'coins': 5, 'cues': 'x'}).encode()).decode()
    g.js(f"document.getElementById('stImp').value='{bad}';document.getElementById('stImpB').click()")
    assert g.js("document.getElementById('stM').textContent") == 'Geçersiz yedek kodu.'
    good = base64.b64encode(json.dumps({'coins': 12345, 'name': 'Yedek', 'cues': ['basic']}).encode()).decode()
    g.js(f"document.getElementById('stImp').value='{good}';document.getElementById('stImpB').click();document.getElementById('stImpB').click()")
    g.page.wait_for_load_state('load'); g.page.wait_for_function("typeof save==='object'&&!!window.bbaReport"); g.wait(1500)
    assert g.js("save.name") == 'Yedek'

def test_dosyaya_yedek_ve_geri_yukleme(game, tmp_path):
    g = game(); g.login('Dosya')
    g.js("save.coins=777;persist();openSettings();stTab='guv';stRender()"); g.wait(200)
    with g.page.expect_download() as d:
        g.js("document.getElementById('stFile').click()")
    p = tmp_path / 'yedek.txt'; d.value.save_as(p)
    assert d.value.suggested_filename.startswith('blackball-yedek-')
    g.js("save.coins=1;save.name='Degisti';persist()")
    g.page.set_input_files('#stFileIn', str(p)); g.wait(400)
    g.js("document.getElementById('stImpB').click()")
    g.page.wait_for_load_state('load'); g.page.wait_for_function("typeof save==='object'&&!!window.bbaReport"); g.wait(1500)
    assert g.js("[save.name,save.coins]") == ['Dosya', 777]

def test_telefonda_kopru_yoksa_sahte_basari_yok(game):
    g = game(); g.login()
    g.js("window.Capacitor={isNativePlatform:()=>true,Plugins:{},registerPlugin:n=>({saveText:()=>Promise.reject({message:'not implemented'})})};openSettings();stTab='guv';stRender()"); g.wait(200)
    g.js("document.getElementById('stFile').click()"); g.wait(300)
    assert 'Kaydedilemedi' in g.js("document.getElementById('stM').textContent")
    g.js("window.Capacitor={isNativePlatform:()=>true,Plugins:{}};document.getElementById('stFile').click()"); g.wait(300)
    assert 'köprüsü yok' in g.js("document.getElementById('stM').textContent")
