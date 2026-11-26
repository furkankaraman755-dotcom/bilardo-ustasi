"""Para akışları: maç ücreti/ödülü, turnuva, kutular, iadeler, rozetler."""
from conftest import no_errors

STEP = r'''()=>{if(!document.getElementById('game').classList.contains('show'))return 'nogame';if(over)return 'over';
 if(moving){let st=0;while(moving&&st<20000){for(let i=0;i<10;i++)physStep(.1);st++;if(!friction()){moving=false;endShot();}}return 'stepped';}
 if(isAI(turn))return 'ai';if(ballInHand){const [x,y]=freeSpot(TW*.2,TH/2);cue.x=x;cue.y=y;}
 const tg=legalTargets(turn);const s=findShots(cue.x,cue.y,tg);
 if(s.length){aim=s[0].aim;power=Math.min(100,Math.max(10,s[0].power));callPk=s[0].pk>=0?s[0].pk:0;}else{const t=tg[0];aim=Math.atan2(t.y-cue.y,t.x-cue.x);power=50;callPk=0;}
 shoot();return 'shot';}'''

def play(g, maxit=3000):
    for _ in range(maxit):
        r = g.js(STEP)
        if r == 'nogame' and g.js("/Maç açılamadı/.test(document.getElementById('dlg').textContent||'')"):
            raise AssertionError('maç açılamadı (ücret iade edildi): ' + str(g.js("localStorage.getItem('bba_err')")))
        if r == 'over': return True
        g.wait(20 if r in ('ai', 'nogame') else 1)
    return False

def test_oda_maci_ucret_ve_odul(game):
    # zamanlayıcılar 4 kat hızlı; daha fazlası feeGuard'ın 16 sn bekçisini eşleşmeden önce tetikleyebilir
    g = game(fast=0.25, seed=777); g.login()
    for ri in (0, 1):
        c0, fee, prize = g.js(f"[save.coins,ROOMS[{ri}].fee,ROOMS[{ri}].prize]")
        lv0, w0 = g.js("[save.level,save.wins]")
        g.js(f"show('rooms');startRoom(ROOMS[{ri}])"); g.wait(100)
        assert g.js("save.coins") == c0 - fee, 'giriş ücreti düşmedi'
        assert play(g), 'maç bitmedi'
        won = 'Kazandın' in g.js("document.getElementById('ot').textContent")
        c1 = g.js("save.coins")
        if won: assert c1 >= c0 - fee + prize, 'ödül eksik'   # seviye ödülü ek gelebilir
        else:
            # kayıpta maç ödülü yok; ama kayıp XP'si seviye atlatırsa seviye ödülü gelebilir — onu ayrıca hesapla
            lv_bonus = g.js(f"(()=>{{let s=0;for(let l={lv0}+1;l<=save.level;l++){{s+=l*250;if(l%10===1)s+=titleReward(Math.floor((l-1)/10)).coins;}}return s;}})()")
            assert c0 - fee <= c1 <= c0 - fee + lv_bonus + 1, ('kayıpta ödül verildi', c0, fee, c1, lv_bonus)
            assert g.js("save.wins") == w0, 'kayıp galibiyet sayıldı'
        assert g.js("!save.live&&!save.pendFee"), 'canlı maç/ücret kaydı kaldı'
        g.js("document.getElementById('omenu').click()")
    no_errors(g)

def test_turnuva_giris_yazisi(game):
    g = game(); g.login()
    c0 = g.js("save.coins"); g.js("document.getElementById('mEv').click()"); g.wait(300)
    g.js("document.getElementById('tStart').click()"); g.wait(2600)
    t = g.js("document.querySelector('#mmScr .mqInfo').textContent")
    assert '1.000' in t and '7.500' in t, t
    assert c0 - g.js("save.coins") == g.js("TOUR.fee")
    g.wait(6000); g.js("leaveGame();startTourRound(1)"); g.wait(1500)
    assert 'Giriş' not in g.js("document.querySelector('#mmScr .mqInfo').textContent")

def test_sandik_cift_basis_ve_tl_paket(game):
    # V6 mağaza: Sandıklar (Dolar ile) çift basışta bir kez düşer; TL paketleri test modunda onayla verilir
    g = game(); g.login()
    g.js("openShop('box')"); g.wait(300)
    assert g.js("document.querySelector('.screen.show').id") == 'shop6'
    c0 = g.js("save.cash"); g.js("V6API.buyChest(SHOP6.SANDIK[0]);setTimeout(()=>V6API.buyChest(SHOP6.SANDIK[0]),200)"); g.wait(2500)
    assert c0 - g.js("save.cash") == 20, 'çift basışta iki kez para düştü'
    g.js("closeDlg()"); c1 = g.js("save.coins")
    g.js("V6API.tlBuy(SHOP6.TL_CIP[0])"); g.wait(200); g.js("document.getElementById('v6y').click()"); g.wait(200)
    assert g.js("save.coins") - c1 == 20000
    g.js("save.cash=3"); c2 = g.js("save.cash"); g.js("window._boxLock=0;V6API.buyChest(SHOP6.SANDIK[2])"); g.wait(200)
    assert g.js("save.cash") == c2, 'para yetmezken sandık açıldı'
    no_errors(g)

def test_iade_sonrasi_mac_acilmaz(game):
    g = game(); g.login()
    c0 = g.js("save.coins"); g.js("show('rooms');startRoom(ROOMS[2])"); g.wait(1000)
    g.js("feeFail('test')"); g.wait(8000)
    assert g.js("save.coins") == c0, 'ücret iade edilmedi'
    assert not g.js("document.getElementById('game').classList.contains('show')"), 'iade sonrası maç açıldı'
    g.js("closeDlg()")

def test_rozet_sadece_ulke_odalarinda(game):
    g = game(); g.login()
    r = g.js("""()=>{const out={};for(const [nm,room] of [['ozel',SPECIAL[0]],['ulke',ROOMS[1]]]){
      startGame('ai','easy',{kind:'match',room,game:room.game||'8',label:'t'});save.rw[room.id]=BADGE_WINS-1;
      save.cues=save.cues.filter(x=>x!=='u_'+room.idx);gameOver(0,'test');out[nm]=save.cues.includes('u_'+room.idx);leaveGame();}return out;}""")
    assert r == {'ozel': False, 'ulke': True}, r
    no_errors(g)

def test_kayipta_odul_yok(game):
    g = game(fast=0.25); g.login()
    c0, fee, prize = g.js("[save.coins,ROOMS[0].fee,ROOMS[0].prize]")
    g.js("show('rooms');startRoom(ROOMS[0])")
    g.page.wait_for_function("document.getElementById('game').classList.contains('show')&&!over", timeout=20000)
    l0 = g.js("save.losses"); g.js("gameOver(1,'test')"); g.wait(300)
    c1 = g.js("save.coins")
    assert g.js("save.losses") == l0 + 1 and 'Kaybettin' in g.js("document.getElementById('ot').textContent")
    assert c0 - fee <= c1 < c0 - fee + prize, (c0, fee, c1)   # sadece olası seviye ödülü gelebilir
    assert g.js("!save.live&&!save.pendFee")
    no_errors(g)
