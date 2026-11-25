"""Açılış ve ekranlar (duman testi, 1-02'nin temeli)."""
from conftest import no_errors

SCREENS_JS = """async()=>{const ids=[...document.querySelectorAll('.screen')].map(e=>e.id).filter(x=>x!=='game');const out=[];
 for(const id of ids){try{show(id);}catch(e){out.push(id+': '+e.message);}await new Promise(r=>setTimeout(r,150));}
 for(const f of ['openProfile','openDaily','openCues','openShop','openMissions','openWheel','openScratch','openAch','openInbox','openSettings','openAvatar','openGifts','openLead']){
   try{window[f]&&window[f]();}catch(e){out.push(f+': '+e.message);}await new Promise(r=>setTimeout(r,250));
   try{closeDlg();}catch(_){}for(const id of ['avs4','gf4','pf4'])document.getElementById(id)&&document.getElementById(id).remove();show('menu');}
 return out;}"""

def test_acilis_hatasiz(game):
    g = game(); g.login(); g.reload()
    assert g.js("document.querySelector('.screen.show').id") == 'menu'
    assert g.js("typeof window.fullFit") == 'function', 'son betikler çalışmamış'
    no_errors(g)

def test_butun_ekranlar_aciliyor(game):
    g = game(); g.login(); g.reload()
    assert g.js(SCREENS_JS) == []
    no_errors(g)

def test_resimli_avatarla_acilis(game):
    # surum-73 öncesi: AV_ART TDZ hatası betiğin kalanını durduruyordu
    g = game(); g.login()
    g.js("save.avatar={img:Object.keys(window.AV_ART)[0],c:'#1f5bff'};persist()"); g.reload()
    assert g.js("typeof window.fullFit") == 'function'
    no_errors(g)

def test_farkli_kayit_durumlari(game):
    g = game()
    cases = [
        "save.slots=[{tier:0,start:0},{tier:1,start:Date.now()},{tier:3,start:1},null]",
        "save.level=999;save.xp=5",
        "save.live={kind:'match',label:'X',t:Date.now()}",
        "save.pendFee={amt:250,t:Date.now(),kind:'room'}",
        "save.table='yok';save.cue='yok'",
    ]
    for c in cases:
        g.js("window._bbaNoSave=0;save.name='Ali';save.pid=1;" + c + ";persist()"); g.reload()
        assert g.js("typeof window.fullFit") == 'function', c
        assert g.js("document.querySelector('.screen.show')!==null"), c
    assert g.js("[save.cue,save.table]") == ['basic', 'pro']
    no_errors(g)
