import array
import time

import rp2
from machine import Pin


class NeoPixel:
    def __init__(self, pin_num=13, num_leds=1, brightness=0.2):
        self.pin = pin_num
        self.num = num_leds
        self.brightness = brightness

        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.ORANGE = (255, 165, 0)
        self.BLACK = (0, 0, 0)

        self.sm = rp2.StateMachine(
            0, self.ws2812, freq=8_000_000, sideset_base=Pin(pin_num)
        )
        self.sm.active(1)
        self.ar = array.array("I", [0 for _ in range(num_leds)])

    # WS2812 PIO program
    @staticmethod
    @rp2.asm_pio(
        sideset_init=rp2.PIO.OUT_LOW,
        out_shiftdir=rp2.PIO.SHIFT_LEFT,
        autopull=True,
        pull_thresh=24,
    )
    def ws2812():
        T1 = 2
        T2 = 5
        T3 = 3
        wrap_target()  # noqa
        label("bitloop")  # noqa
        out(x, 1).side(0)[T3 - 1]  # noqa
        jmp(not_x, "do_zero").side(1)[T1 - 1]  # noqa
        jmp("bitloop").side(1)[T2 - 1]  # noqa
        label("do_zero")  # noqa
        nop().side(0)[T2 - 1]  # noqa
        wrap()  # noqa

    def pixels_set(self, i, color):
        self.ar[i] = (color[1] << 16) + (color[0] << 8) + color[2]

    def pixels_fill(self, color):
        for i in range(len(self.ar)):
            self.pixels_set(i, color)

    def pixels_show(self):
        dimmer_ar = array.array("I", [0 for _ in range(self.num)])
        for i, c in enumerate(self.ar):
            r = int(((c >> 8) & 0xFF) * self.brightness)
            g = int(((c >> 16) & 0xFF) * self.brightness)
            b = int((c & 0xFF) * self.brightness)
            dimmer_ar[i] = (g << 16) + (r << 8) + b
        self.sm.put(dimmer_ar, 8)

    def set_color(self, color):
        self.pixels_fill(color)
        self.pixels_show()

    def pulsate_color(self, color, pulse_duration=2.0, step=0.05):
        for _ in range(int(pulse_duration / (step * 2))):
            for brightness in range(10):
                self.brightness = brightness / 10
                self.set_color(color)
                time.sleep(step)
            for brightness in reversed(range(10)):
                self.brightness = brightness / 10
                self.set_color(color)
                time.sleep(step)
        self.brightness = 0.2
