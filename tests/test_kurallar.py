"""Oyun kuralları ve fizik: 2 kişilik simülasyon, pes etme, yapay zekâ."""
from conftest import no_errors, RUN_SHOT

SIM = r'''(N)=>{const out={games:0,shots:0,errors:[],bad:[]};const bad=m=>{if(out.bad.length<20)out.bad.push(m)};
 for(let gi=0;gi<N;gi++){let calls=0;const g0=gameOver;gameOver=function(){calls++;return g0.apply(this,arguments)};
  startGame('2p',null,{kind:'2p',game:gi%2?'9':'8'});let ns=0;
  while(!over&&ns<300){ns++;
   if(ballInHand){const [x,y]=freeSpot(R+Math.random()*(TW-2*R),R+Math.random()*(TH-2*R));cue.x=x;cue.y=y;}
   const tg=legalTargets(turn);let a=null;
   const s=findShots(cue.x,cue.y,tg);if(s.length&&Math.random()<.8){a=s[0].aim;power=Math.min(100,Math.max(10,s[0].power));callPk=s[0].pk>=0?s[0].pk:0;}
   if(a==null){const t=tg[Math.floor(Math.random()*tg.length)]||balls[1];a=Math.atan2(t.y-cue.y,t.x-cue.x)+(Math.random()-.5)*.2;power=20+Math.random()*80;callPk=0;}
   aim=a;try{shoot();}catch(e){out.errors.push('shoot '+e.message);break;}
   let st=0;try{while(moving&&st<20000){for(let i=0;i<10;i++)physStep(.1);st++;if(!friction()){moving=false;endShot();}}}catch(e){out.errors.push('fizik '+e.message);break;}
   if(st>=20000)bad('toplar durmadı');out.shots++;
   for(const b of balls){if(!isFinite(b.x)||!isFinite(b.y))bad('NaN top '+b.id);if(!b.pot&&(b.x<-R||b.y<-R||b.x>TW+R||b.y>TH+R))bad('masadan kaçan top '+b.id);}
   for(let i=0;i<balls.length;i++)for(let j=i+1;j<balls.length;j++){const A=balls[i],B=balls[j];if(A.pot||B.pot)continue;if(Math.hypot(A.x-B.x,A.y-B.y)<2*R-0.5)bad('iç içe top '+A.id+'-'+B.id);}}
  gameOver=g0;if(!over)bad('oyun bitmedi');if(calls!==1)bad('gameOver '+calls+' kez');out.games++;}
 return out;}'''

def test_iki_kisilik_simulasyon(game):
    g = game(seed=12345)
    r = g.js(SIM, 12)
    assert r['errors'] == [], r['errors']
    assert r['bad'] == [], r['bad']
    assert r['games'] == 12
    no_errors(g)

def test_pes_edince_tek_sonuc(game):
    # surum-73: top yuvarlanırken pes edilip 8 girerse hem kayıp hem galibiyet yazılıyordu
    g = game(); g.login()
    g.js("startGame('ai','easy',{kind:'match',room:ROOMS[1],game:'8',label:'t'})")
    r = g.js("""()=>{let calls=0;const g0=gameOver;gameOver=function(){calls++;return g0.apply(this,arguments)};const s0={w:save.wins,l:save.losses};
      for(const b of balls)if(b.id&&b.id!==8)b.pot=true;const e=balls.find(b=>b.id===8);e.x=TW*.5;e.y=TH*.5;groups=['solid','stripe'];shots=3;
      const q=POCKETS.slice().sort((a,b)=>Math.hypot(a.x-e.x,a.y-e.y)-Math.hypot(b.x-e.x,b.y-e.y))[0];const ang=Math.atan2(q.y-e.y,q.x-e.x);
      cue.x=e.x-Math.cos(ang)*120;cue.y=e.y-Math.sin(ang)*120;aim=ang;power=55;turn=0;ballInHand=false;shoot();forfeit();
      let st=0;while(moving&&st<20000){for(let i=0;i<10;i++)physStep(.1);st++;if(!friction()){moving=false;endShot();}}gameOver=g0;
      return {calls,dw:save.wins-s0.w,dl:save.losses-s0.l,title:document.getElementById('ot').textContent}}""")
    assert r['calls'] == 1 and r['dw'] == 0 and r['dl'] == 1, r
    no_errors(g)

def test_yapay_zeka_bos_hedef(game):
    g = game()
    r = g.js("()=>{startGame('ai','easy',{kind:'free'});for(const b of balls)if(b.id)b.pot=true;turn=1;ballInHand=false;try{aiTurn();return 'ok'}catch(e){return e.message}finally{clearTimeout(aiTimer);leaveGame();}}")
    assert r == 'ok'
    no_errors(g)
