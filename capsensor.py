""" capacitive sensor library attempting using adafruit circuitpython digitalio module """
import digitalio as dio
import time, board

class CapSenor:
    def __init__(self, s_pin, r_pin, timeout = 2, sample_size = 20):
        try: assert s_pin != r_pin
        except AssertionError:
            print("send pin and receive pin cannot be the same")
            raise
        self._sPin = dio.DigitalInOut(s_pin)
        self._sPin.switch_to_output()
        self._rPin = dio.DigitalInOut(r_pin)
        self._rPin.switch_to_input()
        try: assert timeout > 0
        except AssertionError:
            print("timeout value must be a number of seconds > 0")
            raise
        # save timeout & number of iterations per sample 
        self.timeout = timeout
        self.sample = sample_size
        # set zero capacitance baseline as current state
        self.baseline = self.capTime
    
    # measure 5 time constant on circuit attached between send & receive pins
    def m5tConst(self):
        pong = False
        results = []
        avg = 0
        for _ in range(self.sample):
            start = time.monotonic()
            now = start
            self._sPin.value = True
            while now < start + self.timeout or not pong:
                if self._rPin.value:
                    pong = now
                now = time.monotonic()
            self._sPin.value = False
            if pong:
                results.append(pong-start)
            # wait for receive pin to settle back down
            while self._rPin.value: pass
        # take average of results
        avg = self.avg(results)
        # apply band pass filter
        for i, r in results:
            if r > 1.1 * avg or r < 0.9 * avg:
                results.remove(i)
        # now take a more concise average
        avg = self.avg(results)
        results.clear()
        return avg

    # returns the average of the list of results passed as samples
    def avg(self, samples):
        for t in samples:
            avg += t
        avg /= len(samples)
        return avg
    
    @property
    def capTime(self):
        return self.m5tConst()

    # return boolean isPressed
    @property
    def value(self):
        temp = self.capTime
        if temp / 5 > self.baseline:
            return True
        else: return False 