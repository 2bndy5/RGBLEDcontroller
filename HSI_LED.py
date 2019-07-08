import time, math
from colorsys import hsv_to_rgb, rgb_to_hsv

# color to use when not in animation
idleHSI = [0.0, 0.0, 0.5]
# times for corresponding animations in milliseconds
hueTime = 1000
fadeTime = 1000

class HSI_LED:
    def __init__(self, hsi = idleHSI):
        assert len(hsi) == 3
        self._hsi = hsi
        self.last_hsi = hsi # used to remember beginning of transition
    
    def cycleHue(self):
        self.iniHue = int(time.monotonic() * 1000)
        self.endHue = self.iniHue + hueTime
        self.endNorm = self.endHue + fadeTime
        # set Hue = 0.0, Saturation = 1.0, & Intensity = idle intensity if idle is not off else full 
        self._hsi = [0.0, 1.0, idleHSI[2] if idleHSI[2] != 0 else 1.0]
        self.last_hsi = self._hsi
    
    def tick(self):
        if self.last_hsi != idleHSI:
            now = int(time.monotonic() * 1000)
            if now > self.endNorm: # new norm has been set
                self.endHue = now
                self.endNorm = now + self.dt
            
            if now < self.endHue: # cycle hue
                self._hsi[0] = (1 - cos( (now - self.iniHue) / float(self.endHue - self.iniHue) * math.pi ) ) / 2
                self.last_hsi = self._hsi
            elif now <= self.endNorm: # fade to norm
                delta = (1 - cos( (now - self.endHue) / float(self.endNorm - self.endHue) * math.pi ) ) / 2
                for i in range(len(self._hsi)):
                    self._hsi[i] = (idleHSI[i] - self.last_hsi[i]) * delta + self.last_hsi[i]
            else: 
                self.last_hsi = idleHSI
                self._hsi = idleHSI
    
    @property
    def value(self):
        return self._hsi[2]

    @value.setter
    def value(self, v):
        if 0 <= v <= 1:
            idleHSI[2] = v
    
    @property
    def rgb(self):
        return hsv_to_rgb(self._hsi[0], self._hsi[1], self._hsi[2])

    @rgb.setter
    def rgb(self, v):
        for c in v:
            assert 0 <= c <= 1
        if len(v) >= 3:
            idleHSI = rgb_to_hsv(v[0], v[1], v[2])
    
    @property
    def hsi(self):
        return self._hsi

    @hsi.setter
    def hsi(self, v):
        for i, c in v:
            assert 0 <= c <= 1
        if len(v) >= 3:
            idleHSI = hsv_to_rgb(v[0], v[1], v[2])
