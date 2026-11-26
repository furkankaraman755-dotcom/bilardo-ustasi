"""1-02: duman testi + görünüş karşılaştırması.
Bütün ekranlar açılır (hata olmamalı) ve önceki sürümle aynı ortamda çekilip karşılaştırılır.
Bilerek görünüş değiştiren commit mesajına [görünüş] yazılırsa fark raporlanır ama test kırmızı olmaz.
Fark resimleri tests/_cikti/fark/ altına yazılır (CI'da 'test-sonuclari' içinde)."""
import os, subprocess, pytest
from gorunus import ROOT, OUT, SCREENS, prev_dir, shoot, compare

ESIK = 25    # bir ekranda 25'ten fazla piksel belirgin şekilde değiştiyse "görünüş değişti" sayılır (aynı sürümde gürültü 0–1 piksel; bir rakam ≈ 40–250 piksel)

def commit_msg():
    try: return subprocess.run(['git', '-C', str(ROOT), 'log', '-1', '--format=%B'], capture_output=True, text=True).stdout
    except Exception: return ''

def test_duman_ve_gorunus(browser):
    now = OUT / 'simdi'; errs = shoot(browser, ROOT / 'index.html', now)
    assert not errs, f'ekran açılırken hata: {errs}'
    ref = os.environ.get('BBA_PREV_REF', 'HEAD')
    prev = prev_dir(ref)
    if prev is None:
        pytest.skip(f'önceki sürüm ({ref}) bulunamadı; sadece duman testi yapıldı')
    old = OUT / 'onceki'; shoot(browser, prev, old)
    (OUT / 'fark').mkdir(parents=True, exist_ok=True)
    changed = {}
    for name, _ in SCREENS:
        r = compare(old / f'{name}.png', now / f'{name}.png', OUT / 'fark' / f'{name}.png')
        if r > ESIK: changed[name] = r
    rapor = '\n'.join(f'{k}: {v} piksel' for k, v in changed.items()) or 'fark yok'
    (OUT / 'fark_raporu.txt').write_text(rapor, encoding='utf-8')
    if changed and '[görünüş]' not in commit_msg():
        pytest.fail('görünüşü değişen ekranlar (önceki sürüme göre): ' + rapor + ' — bilerek yapıldıysa commit mesajına [görünüş] yaz')
