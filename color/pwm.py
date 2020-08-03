"""PWMOut class as an alternative to circuitpython's pulseio.PWMOut due to lack of support on the
Raspberry Pi and the Jetson and various MicroPython compatible boards"""
# pylint: disable=import-error
MICROPY = False
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False) # unadvised due to thread priority
except ImportError:
    import machine
    MICROPY = True

# example code for Raspberry Pi & nVidia Jetson
# GPIO.setup(12, GPIO.OUT)
# p = GPIO.PWM(12, 50)  # channel=12 frequency=50Hz
# p.start(0) # init duty_cycle of 0 (max of 100)
# p.ChangeFrequency(500)
# for dc in range(0, 101): # fade LED from 0 to 100% duty cycle
#     p.ChangeDutyCycle(dc)
#     time.sleep(0.1)
# p.stop()
# GPIO.cleanup(12) # this should be done on entry & exit of programs

# example code for micropython boards ()
# from machine import Pin, PWM
# pwm0 = PWM(Pin(0))      # create PWM object from a pin
# pwm0.freq()             # get current frequency
# pwm0.freq(1000)         # set frequency
# pwm0.duty()             # get current duty cycle
# pwm0.duty(200)          # set duty cycle
# pwm0.deinit()           # turn off PWM on the pin
# pwm2 = PWM(Pin(2), freq=500, duty=512) # create and configure in one go

class PWMOut:
    """A wrapper class to substitute the RPi.GPIO.PWM or `machine.Pin` for `pulseio.PWMOut`

    :param int,str pin: The pin name/number to be used for PWM output.
        RPi.GPIO is configured to accept an `int` or `str` as the pin's BCM numbering scheme.
        machine.Pin usually accepts an `int` or `str` ordering scheme usually printed on the board.
    :param int freq: The frewquency (in Hz) of the PWM output. Defaults to 500 Hz.
    :param int duty_cycle: The initial duty cycle of the PWM output. Ranges [0, 65535]
    """
    def __init__(self, pin, freq=500, duty_cycle=0):
        self._pin_number = int(repr(pin))
        if MICROPY:
            if freq < 1 or freq > 1000:
                raise ValueError('esp8266 only allows a frequency that ranges 1Hz to 1kHz')
            self._pin = machine.PWM(
                machine.Pin(self._pin_number),
                freq=freq,
                duty=int(duty_cycle * 1023 / 65535))
        else:
            GPIO.cleanup(self._pin_number) # make sure to deinit pin from any previous unresolved usage
            GPIO.setup(self._pin_number, GPIO.OUT)
            self._pin = GPIO.PWM(self._pin_number, freq)
            self._pin.start(duty_cycle / 655.35)
        self._frequency = int(freq)
        self._duty_cycle = int(duty_cycle)

    @property
    def duty_cycle(self):
        """The `int` value in range [0, 65535] of the pin's current PWM duty cycle."""
        return self._duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, val):
        val = max(0, min(65535, int(val)))
        if MICROPY:
            self._pin.duty(int(val * 1023 / 65535))
        else:
            self._pin.ChangeDutyCycle(val / 655.35)
        self._duty_cycle = val

    @property
    def frequency(self):
        """The `int` value of the pin's current (approximated) PWM frequency."""
        return self._frequency

    @frequency.setter
    def frequency(self, freq):
        if MICROPY:
            if freq < 1 or freq > 1000:
                raise ValueError('esp8266 only allows a frequency that ranges 1Hz to 1kHz')
            self._pin.freq(freq)
        else:
            self._pin.ChangeFrequency(freq)
        self._frequency = freq

    def deinit(self):
        """de-initialize the pin for future instantiation."""
        if MICROPY:
            self._pin.deinit()
        else:
            self._pin.stop()
            # make sure to deinit pin from any previous unresolved usage
            GPIO.cleanup(self._pin_number)

    def __del__(self):
        self.deinit()
        del self._pin, self._pin_number, self._frequency, self._duty_cycle
