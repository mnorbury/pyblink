import math
import time

from blink1 import blink1

def make_pulse(target, loop_time):
    def _pulse_signal(x, frequency, count):
            y = x*0.5*(math.cos(math.pi*2*count*loop_time*frequency)+1.0)
            return y
    def pulse_rgb(frequency=1):
        amplitude = [int(x/2.0) for x in target]
        count     = 0
        while True:
            current = [int(_pulse_signal(x, frequency, count)) for x in target]
            yield tuple(current)
            count += 1
    return pulse_rgb

red_pulse = make_pulse((255,0,0),0.1)
green_pulse = make_pulse((0,255,0),0.1)
yellow_pulse = make_pulse((255,255,0),0.1)

client = blink1.Blink1()

rgb_generator = red_pulse()
for i in range(1000):
    client.fade_to_rgb(100,*next(rgb_generator))
    time.sleep(0.1)
