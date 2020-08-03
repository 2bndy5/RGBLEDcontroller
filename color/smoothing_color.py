"""a mixin module that holds all code related to smoothing the input color transitions."""
from math import pi as PI, cos
import time
import color.color


class SmoothColor:
    """mixin class to incorporate smoothing input algorithm on each color.
    
    :param list pins: A list of PWM-capable pins. Each pin should be compatible with
        CircuitPython's PWMOut class.
    :param int ramp_time: The number of milliseconds it should take to transition from
        the current color to the new color.
    :param list,tuple color: The initial color. This `list` or `tuple` should contain
        exactly 3 components where each component is an `int` in range [0, 255] in
        accordance with the RGB color space.
    """

    def __init__(self, pins, ramp_time, init_color):
        self._signals = pins
        self._init_color, self._target_color = init_color, init_color
        self._init_smooth = 1
        self._end_smooth = 0
        self._dt = ramp_time
        super().__init__()

    @property
    def ramp_time(self):
        """This attribute is the maximum amount of time (in milliseconds) used to smooth the input
        values. A negative value will be used as a positive number. Set this to ``0`` to
        disable all smoothing on the color input values or just set the
        `value` attribute directly to bypass the smoothing algorithm.
        """
        return self._dt

    @ramp_time.setter
    def ramp_time(self, delta_t):
        assert delta_t > 0 and isinstance(delta_t, (int, float))
        self._dt = abs(delta_t)

    def write(self, val):
        """This function uses RGB color space to write PWM signal to the LEDs """
        if len(val) == len(self._signals):
            for i, comp in enumerate(val):
                # range of [0, 255] * 257 = range of [0, 65535]
                self._signals[i].duty_cycle = comp * 257

    def sync(self):
        """This function should be used at least once in the application's main loop
        iteration. It will trigger the smoothing input operations on the output value
        if needed. This is not needed if the smoothing algorithms are not utilized/necessary in the application"""
        time_i = int(time.monotonic() * 1000)
        # print('target color: {}, init color: {}'.format(self._target_color, self._init_color))
        # print('time_i: {}'.format(time_i))
        # print('end smoothing: {}, init smooth: {}'.format(self._end_smooth, self._init_smooth))
        if self.is_cellerating and time_i < self._end_smooth and self.ramp_time:
            new_color = []
            delta_color = (
                1
                - cos(
                    (time_i - self._init_smooth)
                    / float(self._end_smooth - self._init_smooth)
                    * PI
                )
            ) / 2
            # print('delta color: {delta_color}')
            for i, c in enumerate(self._init_color):
                new_color.append(int(delta_color * (self._target_color[i] - c) + c))
        else:
            # print('done changing color')
            self.rgb_value = self._target_color

    @property
    def is_cellerating(self):
        """This attribute contains a `bool` indicating if the color is in the midst of
        changing. (read-only)"""
        for i, c in enumerate(self.rgb_value):
            if self._target_color[i] != c:
                return True
        return False

    # let target_color be the percentual target color [0,1]
    def cellerate(self, target_color):
        """A function to smoothly transition the color to a specified target color.

        :param list target_color: The desired target color in which each component is in range
            [0, 255]. Any invalid input components will be clamped to an `int` value in the
            proper range.
        """
        difs = []
        for i, c in enumerate(target_color):
            target_color[i] = max(0, min(255, int(c)))
            difs[i] = abs(self.value[i] - target_color[i])
        max_dif = max(difs[0], difs[1], difs[2])
        self._init_color = self.value
        self._target_color = target_color
        # integer of milliseconds
        self._init_smooth = int(time.monotonic() * 1000)
        delta_time = max_dif / 255
        # print('dt calculated: {}'.format(delta_time))
        self._end_smooth = int(self._init_smooth + delta_time * self.ramp_time)
        self.sync()

    def __del__(self):
        self.value = [0, 0, 0]
        for s in self._signals:
            s.deinit()
        del (
            self._init_color,
            self._target_color,
            self._init_smooth,
            self._end_smooth,
            self._dt,
            self._signals,
        )
        # super().__del__()

