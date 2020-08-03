""" a module that manages the 3 components of a single color """
from .colorsys import hsv_to_rgb, rgb_to_hsv
from .smoothing_color import SmoothColor

class Color(SmoothColor):
    """A data structure to hold the components of a color based on the HSV & RGB color space.
    
    :param list pins: A list of PWM-capable pins. Each pin should be compatible with
        CircuitPython's PWMOut class.
    :param list,tuple,int color: The initial color. If this is of type `list`
        or `tuple`, then the list/tuple should contain exactly 3 components where each
        component is a `float` in range [0.0, 1.0] for HSV solor space or an `int` in
        range [0, 255] for RGB color space. If this is of type `int`, then it is
        assumed to be a 6-digit hexadecimal color code, and it is converted automatically.
    :param int ramp_time: The number of milliseconds it should take to transition from
        the current color to the new color.
    """

    def __init__(self, pins, color=0, ramp_time=1000):
        self._rgb, self._hsv = [0, 0, 0], [0, 0, 0]
        if isinstance(color, (list, tuple)):
            if isinstance(color[0], int):  # for RGB color
                self._rgb = self._check_input(color, c_space="rgb")
                self._hsv = list(rgb_to_hsv(self._rgb[0], self._rgb[1], self._rgb[2]))
            else:
                self._hsv = self._check_input(color, c_space="hsv")
                self._rgb = list(hsv_to_rgb(self._hsv[0], self._hsv[1], self._hsv[2]))
        else:  # treat as an int and let check_input raise the exception if needed
            self._rgb = self._check_input(color)
            self._hsv = list(rgb_to_hsv(self._rgb[0], self._rgb[1], self._rgb[2]))
        super(Color, self).__init__(pins, ramp_time, self._rgb)

    @property
    def hsv_value(self):
        return self._hsv

    @hsv_value.setter
    def hsv_value(self, val):
        val = self._check_input(val, c_space="hsv")
        self._hsv = val
        self._rgb = list(hsv_to_rgb(val[0], val[1], val[2]))
        self.write(self._rgb)

    @property
    def rgb_value(self):
        """This attribute contains the current RGB values of the color for which each component should be in range [0, 255]. An invalid input value will be clamped to an `int` in the proper range."""
        return self._rgb

    @rgb_value.setter
    def rgb_value(self, val):
        val = self._check_input(val, c_space="rgb")
        self._rgb = val
        self._hsv = list(rgb_to_hsv(val[0], val[1], val[2]))
        self.write(self._rgb)

    def _check_input(self, val, c_space="hsv"):
        """ check input values to make sure they're in the correct form """
        if not isinstance(val, (list, tuple)):
            raise ValueError("{} must be a 3-item list".format(c_space))
        elif isinstance(val, int):  # convert hex color code to rgb list
            if val > 0xffffff or val < 0:
                raise ValueError("hex color code outside proper range")
            else:
                c_space = "rgb"
                temp = []
                for i in range(2, -1, -1):
                    temp.append((val & (0xff << (8 * i))) >> (8 * i))
                val = temp
        else:
            raise ValueError("unknown color input: {}".format(val))
        if c_space.endswith("hsv"):
            for c in val:
                if not isinstance(c, float):
                    raise AttributeError("all hsv list elements must be of type float")
                elif not 0 <= c <= 1:
                    raise ValueError(
                        "all hsv list elements must be in range [0.0, 1.0]"
                    )
        elif c_space.endswith("rgb"):
            for c in val:
                if not isinstance(c, int):
                    raise AttributeError("all rgb list elements must be of type int")
                elif not 0 <= c <= 255:
                    raise ValueError(
                        "all rgb list elements must be in range [0, 255]"
                    )
        return list(val)