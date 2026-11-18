import numpy as np, wave
SR = 44100
rng = np.random.default_rng(3)

class Mix:
    def __init__(s, dur):
        s.N = int(SR * dur); s.L = np.zeros(s.N); s.R = np.zeros(s.N)
    def add(s, sig, t, g=1.0, pan=0.0):
        i = int(t * SR)
        if i >= s.N or i < 0: return
        j = min(s.N, i + len(sig)); x = sig[:j - i] * g
        s.L[i:j] += x * (1 - max(0, pan)); s.R[i:j] += x * (1 + min(0, pan))
    def save(s, path, peak=0.89):
        st = np.stack([s.L, s.R], 1)
        st = np.tanh(st * 1.1)
        st *= peak / (np.abs(st).max() + 1e-9)
        n = len(st); f = int(SR * .4); st[-f:] *= np.linspace(1, 0, f)[:, None]
        with wave.open(path, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((st * 32767).astype(np.int16).tobytes())

def T(d): return np.arange(int(SR * d)) / SR

def lp(x, a):  # one-pole lowpass, a in (0,1)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc); y[i] = acc
    return y

def lpf(x, cutoff):  # fast FFT lowpass
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4); return np.fft.irfft(X, len(x))

def hpf(x, cutoff):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 - 1 / (1 + (f / cutoff) ** 4); return np.fft.irfft(X, len(x))

def kick(big=False):
    t = T(.9 if big else .4); f = 42 + 120 * np.exp(-t * 28)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (.5 if big else .16))
    return np.tanh(s * 2)

def boom():  # cinematic hit
    t = T(2.2); f = 38 + 60 * np.exp(-t * 8)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .8)
    n = lpf(rng.standard_normal(len(t)), 900) * np.exp(-t / .35) * .8
    return np.tanh((s + n) * 1.6)

def snare():
    t = T(.25); n = hpf(rng.standard_normal(len(t)), 1500) * np.exp(-t / .07)
    b = np.sin(2 * np.pi * 190 * t) * np.exp(-t / .05)
    return (n * .6 + b * .5)

def hat(op=False):
    t = T(.2 if op else .05); n = hpf(rng.standard_normal(len(t)), 7000)
    return n * np.exp(-t / (.07 if op else .012)) * .4

def tick(f=2400):
    t = T(.035); return np.sin(2 * np.pi * f * t) * np.exp(-t / .006) * .5

def click():
    t = T(.03); n = hpf(rng.standard_normal(len(t)), 2500) * np.exp(-t / .004)
    return n * .7 + np.sin(2 * np.pi * 900 * t) * np.exp(-t / .003) * .3

def whoosh(d=.6, up=True):
    t = T(d); n = rng.standard_normal(len(t))
    env = np.sin(np.pi * t / d) ** 2
    # sweep via mixing two filtered layers
    lo = lpf(n, 600); hi = hpf(n, 2500); k = t / d if up else 1 - t / d
    return (lo * (1 - k) + hi * k) * env * .9

def pop():
    t = T(.12); f = 300 + 900 * np.exp(-t * 40)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .04) * .7

def ding(f=1318.5):
    t = T(1.2); s = sum(np.sin(2 * np.pi * f * m * t) * a for m, a in [(1, 1), (2.01, .35), (3.02, .15)])
    return s * np.exp(-t / .35) * .45

def saw(f, d):
    t = T(d); s = np.zeros(len(t))
    for det in (-.006, 0, .007):
        ph = (t * f * (1 + det)) % 1; s += 2 * ph - 1
    return s / 3

def pad(freqs, d, cutoff=1400, att=.3):
    s = sum(saw(f, d) for f in freqs) / len(freqs)
    s = lpf(s, cutoff); t = T(d)
    return s * np.minimum(1, t / att) * np.minimum(1, (d - t) / .3)

def pluck(f, d=.35, cutoff=2500):
    t = T(d); s = lpf(saw(f, d), cutoff) * np.exp(-t / (d * .35))
    return s

def bassnote(f, d):
    t = T(d); s = np.sin(2 * np.pi * f * t) + .4 * np.sin(4 * np.pi * f * t)
    return np.tanh(s * 1.5) * np.minimum(1, t / .005) * np.exp(-t / (d * .8)) * .6

def note(n):  # midi -> hz
    return 440 * 2 ** ((n - 69) / 12)
