from sfx import *
D=31; m=Mix(D); B=60/100
def marimba(f,d=.5):
    t=T(d); return (np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*f*4*t)*np.exp(-t/.03))*np.exp(-t/.18)*.5
prog=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]
pat=[0,2,1,2,0,1,2,1]
t=0.0;bar=0
while t<27.6:
    ch=prog[bar%4]
    m.add(pad([note(x) for x in ch],4*B,800,.3),t,.12)
    m.add(bassnote(note(ch[0]-12),2*B),t,.3);m.add(bassnote(note(ch[0]-12),2*B),t+2*B,.25)
    for k in range(8):
        tt=t+k*B/2
        m.add(marimba(note(ch[pat[k]]+12)),tt,.22,pan=.25 if k%2 else -.25)
        if k%4==0: m.add(kick(),tt,.35)
        if k%4==2: m.add(snare(),tt,.12)
        m.add(hat(),tt,.12)
    t+=4*B;bar+=1
m.add(ding(note(88)),.15,.5); m.add(boom(),.1,.35)
MSG=[(2.9,'in'),(3.8,'in'),(5.4,'out'),(7.0,'in'),(8.3,'out'),(13.6,'out'),(15.6,'in'),(17.2,'out'),(19.6,'in'),(20.8,'out'),(23.4,'in'),(24.6,'out'),(26.2,'in')]
def send():
    t=T(.15); f=900+700*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/.04)*.5
def recv():
    t=T(.25); return (np.sin(2*np.pi*1046*t)*np.exp(-t/.06)+np.sin(2*np.pi*1568*np.maximum(0,t-.07))*np.exp(-np.maximum(0,t-.07)/.06)*(t>.07))*.35
for tt,s in MSG: m.add(send() if s=='out' else recv(),tt,.8)
m.add(whoosh(.5),27.3,.6); m.add(boom(),27.7,.7)
m.add(pad([note(x) for x in [57,64,69,72]],3.3,1500,.05),27.7,.3); m.add(ding(note(81)),28.5,.4)
m.save('a3.wav')
