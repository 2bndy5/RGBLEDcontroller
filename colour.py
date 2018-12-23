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
            self.i = floor(self.hue / 60.0)
            self.f = self.hue / 60.0 - self.i
		    self.pv = self.intensity * (1 - self.sat)
		    self.qv = self.intensity * (1 - self.sat * self.f)
		    self.tv = self.intensity * (1 - self.sat * (1 - self.f))
            if (self.i <= 0): # red
				red = max(0, min(255, round(self.intensity * 255)))
                #constrain((int)(255 * intensity), 0, 255)
				green = max(0, min(255, round(self.tv * 255)))
                # constrain((int)(255 * tv), 0, 255)
				blue = max(0, min(255, round(self.pv * 255)))
                # constrain((int)(255 * pv), 0, 255)
			elif (self.i == 1):# green
				red = max(0, min(255, round(self.qv * 255)))
                # constrain((int)(255 * qv), 0, 255)
				green = max(0, min(255, round(self.intensity * 255)))
                # constrain((int)(255 * intensity), 0, 255)
				blue = max(0, min(255, round(self.pv * 255)))
                # constrain((int)(255 * pv), 0, 255)
			elif (self.i == 2):
				red = max(0, min(255, round(self.pv * 255)))
                # constrain((int)(255 * pv), 0, 255)
				green = max(0, min(255, round(self.intensity * 255)))
                # constrain((int)(255 * intensity), 0, 255)
				blue = max(0, min(255, round(self.tv * 255)))
                # constrain((int)(255 * tv), 0, 255)
			elif (self.i == 3): # blue
				red = max(0, min(255, round(self.pv * 255)))
                # constrain((int)(255 * pv), 0, 255)
				green = max(0, min(255, round(self.qv * 255)))
                # constrain((int)(255 * qv), 0, 255)
				blue = max(0, min(255, round(self.intensity * 255)))
                # constrain((int)(255 * intensity), 0, 255)
			elif (self.i == 4):
				red = max(0, min(255, round(self.tv * 255)))
                # constrain((int)(255 * tv), 0, 255)
				green = max(0, min(255, round(self.pv * 255)))
                # constrain((int)(255 * pv), 0, 255)
				blue = max(0, min(255, round(self.intensity * 255)))
                # constrain((int)(255 * intensity), 0, 255)
			elif (self.i >= 5):
				red = max(0, min(255, round(self.intensity * 255)))
                # constrain((int)(255 * intensity), 0, 255)
				green = max(0, min(255, round(self.pv * 255)))
                # constrain((int)(255 * pv), 0, 255)
				blue = max(0, min(255, round(self.qv * 255)))
                # constrain((int)(255 * qv), 0, 255)

            