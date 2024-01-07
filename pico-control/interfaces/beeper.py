import time

from machine import PWM
from machine import Pin


class Beeper:
    def __init__(self, pin):
        self.buzzer = PWM(Pin(pin))

    def beep(self, duration, frequency=1000):
        """Emit a beep of a specified duration and frequency."""
        self.buzzer.freq(frequency)
        self.buzzer.duty_u16(32768)
        time.sleep(duration)
        self.buzzer.duty_u16(0)

    def long_beep(self, duration=1):
        """Emit a long beep."""
        self.beep(duration)

    def short_beep(self, duration=0.2):
        """Emit a short beep."""
        self.beep(duration)
