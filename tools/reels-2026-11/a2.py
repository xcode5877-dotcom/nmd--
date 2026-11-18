from sfx import *
import wave
D=30; m=Mix(D)
src=np.frombuffer(wave.open('yaz.wav').readframes(10**9),np.int16).reshape(-1,2).astype(float)/32768
def clipsrc(s0,d):
    a=src[int(s0*SR):int((s0+d)*SR)].copy(); n=len(a); f=int(.08*SR)
    a[:f]*=np.linspace(0,1,f)[:,None]; a[-f:]*=np.linspace(1,0,f)[:,None]; return a
SEG=[[2.8,7.3,0.3],[7.8,12.3,4.2],[12.8,17.6,27.0],[18.1,22.6,38.0]]
for a,b,s in SEG:
    c=clipsrc(s,b-a); i=int(a*SR); j=min(m.N,i+len(c)); m.L[i:j]+=c[:j-i,0]*.55; m.R[i:j]+=c[:j-i,1]*.55
B=60/92
# lofi chords Fmaj7 Em7 Dm7 Cmaj7
prog=[[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59]]
t=0.0;bar=0
while t<24.6:
    ch=prog[bar%4]
    m.add(pad([note(x) for x in ch],4*B,900,.2),t,.16)
    for k in range(4):
        tt=t+k*B
        if k in(0,2): m.add(kick(),tt,.45)
        if k in(1,3): m.add(snare(),tt,.18)
        m.add(hat(),tt+B/2,.25); m.add(hat(),tt,.18)
    m.add(bassnote(note(ch[0]-12),2*B),t,.35); m.add(bassnote(note(ch[0]-12),2*B),t+2*B,.3)
    t+=4*B;bar+=1
# hook hit
m.add(boom(),0.02,.6); m.add(whoosh(.5),2.4,.5)
# scrubs between segments (rewind)
def scrub(d=.5):
    t=T(d); f=300+2500*np.sin(np.pi*t/d)
    s=np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*.15+lpf(rng.standard_normal(len(t)),3000)*.4
    return s*np.sin(np.pi*t/d)
for a,b,s in SEG[1:]: m.add(scrub(.5),a-.5,.7)
for a,b,s in SEG: m.add(pop(),a+.15,.8); m.add(tick(3000),a+.5,.4)
# export
m.add(whoosh(.4),22.65,.5)
for i in range(14): m.add(tick(1500+i*60),23.0+i*0.1,.25)
m.add(ding(),24.45,.6)
# results groove restart
t=24.7
for k in range(int((D-24.7)/(B/2))):
    tt=t+k*B/2
    if k%4==0: m.add(kick(),tt,.6)
    if k%4==2: m.add(snare(),tt,.25)
    m.add(hat(),tt,.2)
m.add(pad([note(x) for x in [53,57,60,64,69]],D-24.7,1300,.3),24.7,.2)
for i in range(16): m.add(tick(2000+i*40),25+i*.1,.3)
m.add(pop(),27.2,.8); m.add(ding(note(84)),27.85,.4)
m.save('a2.wav')
