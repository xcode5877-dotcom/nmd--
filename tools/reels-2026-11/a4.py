from sfx import *
import numpy as np
D=22.5; m=Mix(D); B=60/112
def recv():
    t=T(.25); return (np.sin(2*np.pi*1046*t)*np.exp(-t/.06)+np.sin(2*np.pi*1568*np.maximum(0,t-.07))*np.exp(-np.maximum(0,t-.07)/.06)*(t>.07))*.35
m.add(boom(),0.02,.8); m.add(whoosh(.4),2.45,.6)
prog=[[57,60,64],[53,57,60],[50,53,57],[52,56,59]]
t=2.8;bar=0
while t<19.2:
    ch=prog[bar%4]; m.add(pad([note(x) for x in ch],4*B,1100,.05),t,.15)
    for k in range(8):
        tt=t+k*B/2
        if tt>19.2: break
        if k%4==0: m.add(kick(),tt,.7)
        if k%4==2: m.add(snare(),tt,.3)
        m.add(hat(k%4==3),tt,.3); m.add(bassnote(note(ch[0]-12),B/2*.9),tt,.4 if k%2==0 else .25)
    t+=4*B;bar+=1
for a,b in [(2.8,8.3),(8.3,13.8),(13.8,19.3)]:
    m.add(whoosh(.35),a-.15,.5)
    for i in range(8): m.add(recv(),a+.4+i*.33,.5)
    for i in range(22): m.add(tick(2000+i*30),a+.4+i*.16,.25)
    m.add(boom(),b-1.5,.7); m.add(snare(),b-1.5,.6)
m.add(boom(),19.3,.9); m.add(pad([note(x) for x in [57,64,69,72]],3.2,1600,.05),19.3,.3); m.add(pop(),20.1,.8); m.add(ding(note(84)),20.8,.4)
m.save('a4.wav')
