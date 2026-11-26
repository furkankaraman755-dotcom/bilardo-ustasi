"""1-03 / H-05: yayın derlemesinde (BBA_DEV=false) test parası, kilit açmalar ve kısayollar olmamalı.
CI'daki sed ile aynı değişiklik yapılıp yayın dosyası ayrıca denenir."""
import os, re, shutil
from conftest import ROOT, Game, no_errors

def yayin_dosyasi():
    src = (ROOT / 'index.html').read_text(encoding='utf-8')
    assert src.count('window.BBA_DEV=true;/*DEV*/') == 1, 'DEV satırı bulunamadı (CI sed bozulur)'
    d = ROOT / 'tests' / '_cikti' / 'yayin'
    if d.exists(): shutil.rmtree(d)
    d.mkdir(parents=True)
    out = src.replace('window.BBA_DEV=true;/*DEV*/', 'window.BBA_DEV=false;/*DEV*/')
    assert 'window.BBA_DEV=true' not in out
    (d / 'index.html').write_text(out, encoding='utf-8')
    os.symlink(ROOT / 'a', d / 'a')
    return (d / 'index.html').as_uri()

def test_kaynakta_test_modu_acik(game):
    g = game(); g.login()
    assert g.js("[window.BBA_DEV,TEST_UNLOCK,save.coins>=15e9,KEY]") == [True, True, True, 'bilardo_ustasi_v1']

def test_yayin_surumunde_test_seyleri_yok(browser):
    url = yayin_dosyasi()
    g = Game(browser)
    try:
        g.page.goto(url); g.page.wait_for_function("typeof save==='object'&&!!window.bbaReport"); g.wait(1200)
        assert g.js("[window.BBA_DEV,TEST_UNLOCK,KEY]") == [False, False, 'bilardo_ustasi_v1_yayin']
        assert g.js("[save.coins,save.cash,save.gems]") == [1000, 5, 10], 'yayında test parası verildi'
        assert g.js("save.cues") == ['basic'], 'yayında ıstakalar açık'
        g.js("save.name='Yeni';save.pid=1;persist()")
        # 5 dokunuş kısayolu bir şey vermemeli
        g.js("show('menu')"); g.wait(200)
        c0 = g.js("save.coins"); g.js("for(let i=0;i<6;i++)document.getElementById('mcoins').click()")
        assert g.js("save.coins") == c0, 'yayında 5 dokunuş para verdi'
        # seviye kilitli masalar kilitli
        g.js("renderRooms();show('rooms')"); g.wait(200)
        assert g.js("document.querySelectorAll('#rooms .room.lock').length") > 0, 'yayında masa kilitleri açık'
        g.js("openSettings();stTab='hak';stRender()"); g.wait(200)
        assert 'TEST MODU' not in g.js("document.querySelector('.stAbout').textContent")
        # aynı telefonda duran test kaydı (15B) yayın sürümüne karışmamalı: Game() önce test sürümünü açtığı için o kayıt burada zaten var
        assert g.js("localStorage.getItem('bilardo_ustasi_v1')") is not None and g.js("save.coins") < 1e6
        no_errors(g)
    finally:
        g.close()
