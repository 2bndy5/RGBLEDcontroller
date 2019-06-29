import time, math

idleHSI = [0.0, 0.0, 0.5]

class Ripple:
    def __init__(self, start, segments = 12):
        self.MaxStages = segments / 2
        self._it = 1
        self.start = start
        self.wave = [] # end points of ripple
    
    def fx(self):
        if 0 < self._it <= self.MaxStages:
            #set left point of ripple wave fx          
            self.wave[0] = self.start + self._it - self.MaxStages * 2 if self.start + self._it >= self.MaxStages * 2 else self.start + self._it
            # set right point of ripple wave fx
            self.wave[1] = 2 * self.MaxStages - (self._it - self.start) if self._it > self.start else self.start - self._it
            self._it += 1 # iterate iterator
        else:
            self.wave = [self.start]
        return self.wave
# end Ripple class

class fxQ:
    def __init__(self, maxSize = 12):
        self._q = []
        self.maxSize = maxSize

    def __getattr__(self, key):
        assert 0 <= key < len(self._q)
        return self._q[key]

    def isIn(self, x):
        if 0 <= x <= self.maxSize:
            for i in range(len(self._q)):
                if self._q[i].start == x:
                    return i
            return None
        else: return None
    
    def pop(self, x):
        isIn = self.isIn(x)
        if isIn is not None : self._q.remove(isIn)

    def push(self, x):
        self.pop(x)
        self._q.append(Ripple(x, self.maxSize))
    
class Pixel:
    def __init__(self, hsi = idleHSI, rampTime = 1000):
        self.dt = rampTime
        assert len(hsi) == 3
        self.hsi = hsi
        self.last_hsi = hsi # used to remember beginning of transition
    
    def cycleHue(self):
        self.iniHue = int(time.monotonic() * 1000)
        self.endHue = self.iniHue + self.dt
        self.endNorm = self.endHue + self.dt
        # set Hue = 0.0, Saturation = 1.0, & Intensity = idle intensity if idle is not off else full 
        self.hsi = [0.0, 1.0, idleHSI[2] if idleHSI[2] != 0 else 1.0]
        self.last_hsi = self.hsi
    
    def tick(self):
        if self.last_hsi != idleHSI:
            now = int(time.monotonic() * 1000)
            if now > self.endNorm: # new norm has been set
                self.endHue = now
                self.endNorm = now + self.dt
            
            if now < self.endHue: # cycle hue
                self.hsi[0] = (1 - cos( (now - self.iniHue) / float(self.endHue - self.iniHue) * math.pi ) ) / 2
                self.last_hsi = self.hsi
            elif now <= self.endNorm: # fade to norm
                delta = (1 - cos( (now - self.endHue) / float(self.endNorm - self.endHue) * math.pi ) ) / 2
                for i in range(len(self.hsi)):
                    self.hsi[i] = (idleHSI[i] - self.last_hsi[i]) * delta + self.last_hsi[i]
            else: 
                self.last_hsi = idleHSI
                self.hsi = idleHSI

