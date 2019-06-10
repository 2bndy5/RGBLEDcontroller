
class Ripple:
    def __init__(self, start, segments = 12):
        self.MaxStages = segments / 2
        self._it = 1
        self.start = start
        self.wave = []
    
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
    
