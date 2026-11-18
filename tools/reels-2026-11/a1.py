from sfx import *
D=25; m=Mix(D); B=0.5  # 120bpm
# intro sting
m.add(boom(),0.05,1.0); m.add(whoosh(.7),0,0.6)
for i,n in enumerate([62,66,69,74]): m.add(pluck(note(n),.5),0.1+i*0.12,.35)
m.add(pad([note(50),note(57),note(62),note(66)],2.2,1800),0.1,.35)
# groove 2.35 -> 23.8 : D minor news drive
prog=[(50,[62,65,69]),(46,[58,62,65]),(48,[60,64,67]),(45,[57,61,64])]
t=2.35; bar=0
while t<23.7:
    root,ch=prog[bar%4]
    m.add(pad([note(x) for x in ch],4*B,1200,.05),t,.18)
    for k in range(8):
        tt=t+k*B/2
        if tt>23.7: break
        m.add(bassnote(note(root-12),B/2*.9),tt,.55 if k%2==0 else .35)
        m.add(hat(k%4==3),tt,.5)
        if k%4==0: m.add(kick(),tt,.9)
        if k%4==2: m.add(snare(),tt,.45)
        m.add(pluck(note(ch[k%3]+12),.2,3500),tt,.12,pan=.3 if k%2 else -.3)
    t+=4*B; bar+=1
for c in [2.35,9.55,13.4,19.8]: m.add(whoosh(.55),c-.28,.8); m.add(boom(),c,.5)
# counters
for i in range(26): m.add(tick(2200+i*30),3+i*0.085,.35)
for i in range(18): m.add(tick(1800+i*40),10+i*0.09,.35)
m.add(pop(),11.6,.9); m.add(ding(),11.62,.6)
for i in range(16): m.add(tick(2000+i*30),15+i*0.12,.3)
# typing
import numpy as np
ts=np.linspace(20.6,22.2,14)
for x in ts: m.add(click(),x+rng.uniform(-.02,.02),.6)
m.add(pop(),22.4,.9)
# end sting
m.add(boom(),23.8,1.0); m.add(whoosh(.5),23.5,.6)
m.add(pad([note(50),note(57),note(62),note(69)],1.2,2000,.02),23.8,.4)
m.add(ding(note(86)),23.85,.4)
m.save('a1.wav')
