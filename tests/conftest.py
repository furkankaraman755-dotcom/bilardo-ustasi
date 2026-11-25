"""Blackball Arena otomatik testleri (GOREV_HARITASI 1-01).
Çalıştırma: pytest -q tests   (Playwright + Chromium gerekir)
Yerelde Chrome yolu BBA_CHROME ile verilebilir; CI'da Playwright'ın kendi Chromium'u kullanılır."""
import os, pathlib, pytest
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / 'index.html').as_uri()
IGNORE = ('ERR_FILE_NOT_FOUND', 'net::ERR_')

@pytest.fixture(scope='session')
def browser():
    with sync_playwright() as p:
        kw = {'args': ['--allow-file-access-from-files', '--autoplay-policy=no-user-gesture-required']}
        if os.environ.get('BBA_CHROME'):
            kw['executable_path'] = os.environ['BBA_CHROME']
        b = p.chromium.launch(**kw)
        yield b
        b.close()

class Game:
    """Bir sayfa + toplanan hatalar. g.js('...') sayfada çalıştırır."""
    def __init__(self, browser, fast=1, w=915, h=412, init='', seed=None):
        self.ctx = browser.new_context(viewport={'width': w, 'height': h}, has_touch=True, accept_downloads=True)
        if fast != 1:  # zamanlayıcıları hızlandır (eşleşme, yapay zekâ düşünme süresi)
            # 5 sn ve üstü süreler (feeGuard bekçisi, 30 sn kuralı) hızlandırılmaz; yoksa yük altında maç haklı olarak iptal edilir
            self.ctx.add_init_script(f"""(()=>{{const F={fast};const st=window.setTimeout;window.setTimeout=(f,ms,...a)=>st(f,(ms||0)>=5000?ms:(ms||0)*F,...a);
              const si=window.setInterval;window.setInterval=(f,ms,...a)=>si(f,Math.max(4,(ms||0)*F),...a);}})();""")
        if seed is not None:  # tekrar üretilebilir rastgelelik (mulberry32)
            self.ctx.add_init_script(f"(()=>{{let a={int(seed)}>>>0;Math.random=function(){{a=(a+0x6D2B79F5)>>>0;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296;}};}})();")
        # her test temiz hata kaydıyla başlar (sayfa yenilenince silinmez)
        self.ctx.add_init_script("try{if(!sessionStorage.getItem('bbaT')){sessionStorage.setItem('bbaT','1');localStorage.removeItem('bba_err');}}catch(_){}")
        if init:
            self.ctx.add_init_script(init)
        self.page = self.ctx.new_page()
        self.errors = []
        self.page.on('pageerror', lambda e: self.errors.append('PAGEERR ' + str(e)))
        self.page.on('console', lambda m: self.errors.append('CONSOLE ' + m.text) if m.type == 'error' and not any(x in m.text for x in IGNORE) else None)
        self.page.goto(URL)
        self.page.wait_for_function("typeof save==='object'&&typeof show==='function'&&!!window.bbaReport")
        self.wait(1500)
    def js(self, code, arg=None):
        return self.page.evaluate(code, arg) if arg is not None else self.page.evaluate(code)
    def wait(self, ms):
        self.page.wait_for_timeout(ms)
    def reload(self):
        self.js("window._bbaNoSave=1;location.reload()")
        self.page.wait_for_load_state('load')
        self.page.wait_for_function("typeof save==='object'&&!!window.bbaReport")
        self.wait(1500)
    def login(self, name='Test', pid=123456):
        self.js(f"save.name={name!r};save.pid={pid};persist()")
    def close(self):
        self.ctx.close()

@pytest.fixture
def game(browser):
    made = []
    def make(**kw):
        g = Game(browser, **kw); made.append(g); return g
    yield make
    for g in made:
        try: g.close()
        except Exception: pass

def no_errors(g, allow=('kayıt', 'test')):
    assert not g.errors, 'konsol/sayfa hatası: ' + ' | '.join(g.errors[:5])
    # try/catch ile yutulup bbaLog'a giden hatalar da yakalanır (ör. açılışta TDZ)
    logged = g.js("JSON.parse(localStorage.getItem('bba_err')||'[]')")
    bad = [x for x in logged if not any(a in (x.get('s') or '') for a in allow)]
    assert not bad, 'hata kaydına düşen hata: ' + ' | '.join(x['m'] + ' (' + (x.get('s') or '') + ')' for x in bad[:5])

# Fiziği elle ilerleten yardımcı (oyun döngüsünü beklemeden atışı bitirir)
RUN_SHOT = """()=>{let st=0;while(moving&&st<20000){for(let i=0;i<10;i++)physStep(.1);st++;if(!friction()){moving=false;endShot();}}return st;}"""
