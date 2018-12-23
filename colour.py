from math import floor

class colour:
    def __init__(self, h = 0, s = 0, i = 0):
        self.hue = h
        self.sat = s
        self.intensity = h
        self.red = 0
        self.green = 0
        self.blue = 0
        self.convert()

    def convert(self):
        if (self.intensity <= 0):
            self.red = 0
            self.green = 0
            self.blue = 0
        elif (self.sat <= 0):
            self.red = max(0, min(255, round(self.intensity * 255)))
            self.green = max(0, min(255, round(self.intensity * 255)))
            self.blue = max(0, min(255, round(self.intensity * 255)))
        else:
            self.temp_i = floor(self.hue / 60.0)
            self.f = self.hue / 60.0 - self.temp_i
            self.pv = self.intensity * (1 - self.sat)
            self.qv = self.intensity * (1 - self.sat * self.f)
            self.tv = self.intensity * (1 - self.sat * (1 - self.f))
            if (self.temp_i <= 0): # red
                self.red = max(0, min(255, round(self.intensity * 255)))
                #constrain((int)(255 * intensity), 0, 255)
                self.green = max(0, min(255, round(self.tv * 255)))
                # constrain((int)(255 * tv), 0, 255)
                self.blue = max(0, min(255, round(self.pv * 255)))
                # constrain((int)(255 * pv), 0, 255)
            elif (self.temp_i == 1):# green
                self.red = max(0, min(255, round(self.qv * 255)))
                # constrain((int)(255 * qv), 0, 255)
                self.green = max(0, min(255, round(self.intensity * 255)))
                # constrain((int)(255 * intensity), 0, 255)
                self.blue = max(0, min(255, round(self.pv * 255)))
                # constrain((int)(255 * pv), 0, 255)
            elif (self.temp_i == 2):
                self.red = max(0, min(255, round(self.pv * 255)))
                # constrain((int)(255 * pv), 0, 255)
                self.green = max(0, min(255, round(self.intensity * 255)))
                # constrain((int)(255 * intensity), 0, 255)
                self.blue = max(0, min(255, round(self.tv * 255)))
                # constrain((int)(255 * tv), 0, 255)
            elif (self.temp_i == 3): # blue
                self.red = max(0, min(255, round(self.pv * 255)))
                # constrain((int)(255 * pv), 0, 255)
                self.green = max(0, min(255, round(self.qv * 255)))
                # constrain((int)(255 * qv), 0, 255)
                self.blue = max(0, min(255, round(self.intensity * 255)))
                # constrain((int)(255 * intensity), 0, 255)
            elif (self.temp_i == 4):
                self.red = max(0, min(255, round(self.tv * 255)))
                # constrain((int)(255 * tv), 0, 255)
                self.green = max(0, min(255, round(self.pv * 255)))
                # constrain((int)(255 * pv), 0, 255)
                self.blue = max(0, min(255, round(self.intensity * 255)))
                # constrain((int)(255 * intensity), 0, 255)
            elif (self.temp_i >= 5):
                self.red = max(0, min(255, round(self.intensity * 255)))
                # constrain((int)(255 * intensity), 0, 255)
                self.green = max(0, min(255, round(self.pv * 255)))
                # constrain((int)(255 * pv), 0, 255)
                self.blue = max(0, min(255, round(self.qv * 255)))
                # constrain((int)(255 * qv), 0, 255)
    # end convert() HSI to RGB

    def setH(self, h):
        self.hue = max(0, min(360, h))
        self.convert()
    def setI(self, i):
        self.intensity = max(0.0, min(1.0, i))
        self.convert()
    def setS(self, s):
        self.sat = max(0.0, min(1.0, s))
        self.convert()
    