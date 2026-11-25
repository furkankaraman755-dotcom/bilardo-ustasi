"""İsim ve yedek kodu üzerinden kod çalıştırılamaması."""
import base64, json
from conftest import no_errors

def test_isimde_html_calismaz(game):
    g = game()
    g.js("save.name='<img src=x onerror=window._x=1>';save.pid=1;localStorage.setItem(KEY,JSON.stringify(save))"); g.reload()
    assert '<' not in g.js("save.name")
    g.js("show('rooms');startRoom(ROOMS[0])"); g.wait(2500)
    assert g.js("window._x||0") == 0
    assert g.js("cleanName('Şükrü Öğün Çağ')") == 'Şükrü Öğün Çağ'

def test_zararli_yedek_temizlenir(game):
    g = game()
    o = {'coins': 1, 'name': 'Y', 'cues': ['basic'], 'pid': '<b>1</b>', 'avatar': {'e': '<img src=x onerror=window._x=1>', 'c': 'red;x'},
         'inbox': [{'id': 1, 'ic': '<i>', 't': '<img src=x onerror=window._x=2>', 'txt': 'a<b>b'}]}
    g.js("o=>{localStorage.setItem(KEY,JSON.stringify(o))}", o); g.reload()
    g.js("show('menu');openInbox()"); g.wait(400); g.js("closeDlg();openProfile()"); g.wait(400)
    assert g.js("window._x||0") == 0
    assert g.js("[save.pid,JSON.stringify(save.avatar)]") == [0, '{}']
