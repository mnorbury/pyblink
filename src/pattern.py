'''
pattern.py - Module for creating light patterns.

Author:
    Martin Norbury (mnorbury@lcogt.net)

July 2014
'''
import itertools
from math import cos, pi

def pattern_factory(loop_time, decay_time = None):
    ''' Create a pattern. '''

    def _signal(amplitude, frequency, time):
        ''' Light signal for a given channel. '''

        decay = max((decay_time - time)/decay_time, 0.1) if decay_time else 1
        y = decay * amplitude * (cos(pi * 2 * time * frequency) + 1.0)

        return int(y)

    def pulse_rgb(target, frequency=1):
        ''' Pulse the RGB channels. '''

        amplitude = [int(channel / 2.0) for channel in target]
        for count in itertools.count():
            time = count * loop_time
            current = [_signal(channel, frequency, time) for channel in amplitude]
            yield tuple(current)

    return pulse_rgb

