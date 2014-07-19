'''
pattern.py - Module for creating light patterns.

:author: Martin Norbury
'''
import itertools
from math import cos, pi, ceil

def pulse_rgb(rgb, loop_time, frequency=1, decay_time=None):
    ''' Pulse the RGB channels.

    :param rgb: The target RGB e.g. (255, 0, 0)
    :param loop_time: The time between each loop call e.g. 0.1s
    :param frequency: The frequency of the pulse (default 1Hz)
    :param decay_time: The amplitude decay time (s)

    :return: A generator.
    '''

    for count in itertools.count():
        time = count * loop_time
        current = [_cosine(channel, frequency, time, decay_time)
                   for channel in rgb]
        yield tuple(current)

def _cosine(amplitude, frequency, time, decay_time):
    ''' Light signal for a given channel. '''

    decay = max((decay_time - time)/decay_time, 0.1) if decay_time else 1
    y = decay * amplitude * (cos(pi * 2 * time * frequency) + 1.0)/2.0

    return ceil(y)

