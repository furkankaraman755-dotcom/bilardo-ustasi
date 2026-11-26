"""Gerçek parmak dokunuşu (surum-76 dersi): .click() ile çalışan düğme, üstünde görünmez katman varsa telefonda çalışmaz.
Her yeni ekrandaki her düğmenin merkezine dokunulur; düğme dokunuşu almalı."""
from conftest import URL, no_errors

SETUP = {
    'menü': "show('menu')",
    'giriş': "show('login')",
    'giriş-pencere': "show('login');[...document.querySelectorAll('#login .v6h')].find(b=>b.getAttribute('aria-label')==='GİRİŞ YAP').click()",
    'üye-pencere': "show('login');[...document.querySelectorAll('#login .v6h')].find(b=>b.getAttribute('aria-label')==='ÜYE OL').click()",
    'dil-pencere': "show('login');[...document.querySelectorAll('#login .v6h')].find(b=>b.getAttribute('aria-label')==='Dil').click()",
    'mağaza-özel': "openShop6('ozel')", 'mağaza-çip': "openShop6('cip')", 'mağaza-dolar': "openShop6('dolar')", 'mağaza-sandık': "openShop6('sandik')",
    'masalar': "openTables6()",
}
SCOPE = {'giriş-pencere': '#login .v6m .v6h', 'üye-pencere': '#login .v6m .v6h', 'dil-pencere': '#login .v6m .v6h', 'giriş': '#login .v6>.v6h', 'menü': '#menu .v6h'}
RESET = """()=>{try{closeDlg()}catch(_){}for(let i=0;i<6;i++){try{if(bbaBack()==='exit')break;}catch(_){break;}}try{closeDlg()}catch(_){}
 for(const id of ['pf4','gf4','avs4'])document.getElementById(id)&&document.getElementById(id).remove();}"""

def test_butun_v6_dugmeleri_dokunusla_calisir(browser):
    ctx = browser.new_context(viewport={'width': 915, 'height': 412}, device_scale_factor=2.625, has_touch=True, is_mobile=True)
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_function("typeof save==='object'&&!!window.V6API"); pg.wait_for_timeout(1500)
    pg.evaluate("save.name='Ali';save.pid=1;persist()")
    bad = []; tot = 0
    for k, js in SETUP.items():
        sel = SCOPE.get(k, '.screen.show .v6h')
        pg.evaluate(RESET); pg.evaluate(js); pg.wait_for_timeout(300)
        n = pg.evaluate(f"[...document.querySelectorAll({sel!r})].filter(b=>b.offsetParent).length")
        for i in range(n):
            pg.evaluate(RESET); pg.evaluate(js); pg.wait_for_timeout(150)
            r = pg.evaluate(f"""(i)=>{{const b=[...document.querySelectorAll({sel!r})].filter(b=>b.offsetParent)[i];if(!b)return null;window._hit=0;
                b.addEventListener('click',()=>window._hit=1,{{once:true,capture:true}});const r=b.getBoundingClientRect();return [b.getAttribute('aria-label'),r.left+r.width/2,r.top+r.height/2]}}""", i)
            if not r: continue
            tot += 1; pg.touchscreen.tap(r[1], r[2]); pg.wait_for_timeout(80)
            if not pg.evaluate("window._hit"): bad.append((k, r[0]))
    ctx.close()
    assert tot >= 100, tot
    assert not bad, 'dokunuşla çalışmayan düğmeler: ' + str(bad)
