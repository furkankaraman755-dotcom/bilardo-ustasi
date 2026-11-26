"""1-02: ekran görüntüsü karşılaştırma yardımcıları.
Aynı ortamda iki sürüm (önceki commit ve şimdiki dosya) çekilir ve karşılaştırılır; böylece yazı tipi/tarayıcı farkı olmaz."""
import datetime, os, pathlib, shutil, subprocess
from PIL import Image, ImageChops

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'tests' / '_cikti'

# (ad, kurulum JS'i) — her ekran temiz bir sayfada, sabit kayıtla çekilir
SCREENS = [
    ('giris', "show('login')"),
    ('menu', "show('menu')"),
    ('odalar', "renderRooms();show('rooms')"),
    ('etkinlikler', "renderEvents();show('events')"),
    ('ozel_oyun', "renderPriv();show('priv')"),
    ('magaza_kutu', "openShop('box')"),
    ('magaza_teklif', "openShop('offer')"),
    ('magaza_masa', "openShop('tables')"),
    ('magaza_ucretsiz', "openShop('free')"),
    ('istakalar', "openCues()"),
    ('liderlik', "openLead()"),
    ('profil', "openProfile()"),
    ('hediyeler', "openGifts()"),
    ('avatar', "openAvatar()"),
    ('ayar_genel', "openSettings();stTab='gen';stRender()"),
    ('ayar_ses', "openSettings();stTab='ses';stRender()"),
    ('ayar_hesap', "openSettings();stTab='hes';stRender()"),
    ('ayar_guvenlik', "openSettings();stTab='guv';stRender()"),
    ('ayar_gorunum', "openSettings();stTab='gor';stRender()"),
    ('ayar_hakkinda', "openSettings();stTab='hak';stRender()"),
    ('gunluk', "openDaily()"),
    ('cark', "openWheel()"),
    ('oyun', "startGame('ai','easy',{kind:'free'})"),
]

# Hareketli şeyler (CSS animasyonları, parçacık tuvalleri, saat) donduruluyor; rastgelelik tohumlu
FREEZE_JS = """(()=>{let a=4242>>>0;Math.random=function(){a=(a+0x6D2B79F5)>>>0;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296;};
 const st=document.createElement('style');st.textContent='*,*::before,*::after{animation-play-state:paused!important;animation-delay:-0.5s!important;transition:none!important;caret-color:transparent!important}';
 document.addEventListener('DOMContentLoaded',()=>document.head.append(st));})();"""
# Sabit kayıt sayfa açılmadan yazılır (sayaç animasyonu ekran görüntüsüne karışmasın); test parası bayrakları dolu
PRESAVE_JS = """(()=>{try{const o={name:'Test',pid:123456,coins:1234567,cash:89,gems:12,level:7,xp:10,avatar:{e:'🐉',c:'#9b30ff'},test5b:1,test10b:1};
 for(const k of ['bilardo_ustasi_v1','bilardo_ustasi_v1_yayin'])localStorage.setItem(k,JSON.stringify(o));localStorage.removeItem('bilardo_ustasi_v1_b');}catch(_){}})();"""
SAVE_JS = """()=>{}"""
MASK_JS = """()=>{try{cancelAnimationFrame(coinRaf);window._coinWait=0;window._coinFlown=save.coins;coinShown=save.coins;setCv(save.coins);}catch(_){} /* sayaç animasyonunu son değere sabitle */
 for(const c of document.querySelectorAll('canvas')){const id=c.id||'';if(/ldFx|bg|fx|part|spark/i.test(id+' '+c.className))c.style.visibility='hidden';}
 for(const v of document.querySelectorAll('video')){try{v.pause();}catch(_){}v.style.visibility='hidden';} /* kutu videoları her an farklı karede */
 for(const c of document.querySelectorAll('canvas.fxCv'))c.style.visibility='hidden'; /* ıstaka efekt tuvalleri zamanla çiziliyor */
 for(const id of ['intro'])document.getElementById(id)&&document.getElementById(id).remove();}"""

def prev_dir(ref):
    """Önceki commit'teki index.html'i a/ klasörüyle birlikte geçici bir klasöre koyar."""
    try:
        html = subprocess.run(['git', '-C', str(ROOT), 'show', f'{ref}:index.html'], capture_output=True, check=True).stdout
    except Exception:
        return None
    d = OUT / 'onceki_surum'
    if d.exists(): shutil.rmtree(d)
    d.mkdir(parents=True)
    (d / 'index.html').write_bytes(html)
    os.symlink(ROOT / 'a', d / 'a')
    return d / 'index.html'

def shoot(browser, html_path, out, w=915, h=412):
    out.mkdir(parents=True, exist_ok=True)
    errs = {}
    for name, setup in SCREENS:
        ctx = browser.new_context(viewport={'width': w, 'height': h}, has_touch=True)
        ctx.add_init_script(FREEZE_JS)
        ctx.add_init_script(PRESAVE_JS)
        pg = ctx.new_page()
        pg.clock.set_fixed_time(datetime.datetime(2026, 11, 20, 12, 0, 0))
        e = []
        pg.on('pageerror', lambda x, e=e: e.append(str(x)))
        pg.goto(pathlib.Path(html_path).as_uri())
        pg.wait_for_function("typeof save==='object'&&typeof show==='function'")
        pg.wait_for_timeout(800)
        pg.evaluate(SAVE_JS)
        try:
            pg.evaluate(setup)
        except Exception as x:
            e.append(str(x))
        pg.wait_for_timeout(900)
        pg.evaluate("async()=>{try{await document.fonts.ready;}catch(_){}await Promise.all([...document.images].map(i=>i.complete?0:(i.decode?i.decode().catch(()=>0):0)));}")
        pg.evaluate(MASK_JS)
        pg.wait_for_timeout(100)
        pg.screenshot(path=str(out / f'{name}.png'))
        if e: errs[name] = e
        ctx.close()
    return errs

def compare(a, b, diff_out, tol=40):
    """Farklı piksel sayısını döndürür (boyut farklıysa çok büyük sayı); fark resmini kaydeder."""
    A = Image.open(a).convert('RGB'); B = Image.open(b).convert('RGB')
    if A.size != B.size: return 10**9
    D = ImageChops.difference(A, B).convert('L').point(lambda v: 255 if v > tol else 0)
    n = D.histogram()[255]
    if n:
        vis = Image.blend(B, Image.new('RGB', B.size, (255, 0, 80)), 0.0)
        vis.paste((255, 0, 80), mask=D)
        side = Image.new('RGB', (A.size[0] * 2, A.size[1])); side.paste(A, (0, 0)); side.paste(vis, (A.size[0], 0))
        side.save(diff_out)
    return n
