"""Ödüllerin kaybolmaması: çark, kart, kutu penceresi, gelen kutusu."""
from conftest import no_errors

def test_cark_yarida_kalirsa_odul_verilir(game):
    g = game(); g.login()
    g.js("save.wheel=0;openWheel();document.getElementById('whGo').click()"); g.wait(600)
    assert g.js("!!save.pendRw")
    g.reload()
    assert g.js("!save.pendRw") and 'Şans Çarkı' in g.js("save.inbox[0].t")
    no_errors(g)

def test_kart_kazinmadan_kapatilirsa_odul_verilir(game):
    g = game(); g.login()
    g.js("save.scrDay=0;openScratch();const r=Math.random;let n=0;Math.random=()=>n++<1?0.1:r();document.getElementById('scGo').click();Math.random=r")
    assert g.js("!!save.pendRw"), 'kazanan kart beklenen ödülü kaydetmedi'
    s0 = g.js("JSON.stringify([save.coins,save.cash,save.gems])")
    g.js("document.getElementById('scX').click()"); g.wait(200)
    assert g.js("!save.pendRw") and g.js("JSON.stringify([save.coins,save.cash,save.gems])") != s0
    no_errors(g)

def test_kutu_penceresi_ezilince_hata_yok(game):
    g = game(); g.login()
    g.js("showLoot('T','#fff','📦',[{coins:100}]);setTimeout(()=>openDaily(),300)"); g.wait(1800)
    g.js("closeDlg();showLoot('A','#fff','📦',[{coins:111}]);setTimeout(()=>showLoot('B','#fff','📦',[{coins:222}]),300)"); g.wait(2000)
    assert '222' in g.js("document.getElementById('chRes').textContent")
    no_errors(g)

def test_gelen_kutusu_sinirlari(game):
    g = game(); g.login()
    r = g.js("""()=>{save.inbox=[];for(let i=0;i<150;i++)save.inbox.push({id:i,ic:'x',t:'m'+i,txt:'',rw:i%3===0?{coins:1}:undefined});
      const g=lgState();g.hist=Array(60).fill({sid:1});g.done=Array(300).fill(0).map((_,i)=>'d'+i);g.paid=Array(100).fill(0).map((_,i)=>i);persist();
      const k=JSON.parse(localStorage.getItem(KEY));return [k.inbox.length,k.inbox.filter(m=>m.rw).length,k.lg.hist.length,k.lg.done.length,k.lg.paid.length]}""")
    assert r == [63, 50, 24, 80, 40], r   # son 20 + alınmamış 43 ödül; hiçbir ödül silinmez
