"""
pattern.py - Module for creating light patterns.

:author: Martin Norbury (martin.norbury@gmail.com)
"""
import itertools
from math import cos, pi, ceil, floor
import webcolors


def color_sequence(targets, ramp_time=10):
    """ Generate a color sequence.

    :param targets: Target colors e.g. ['red', 'blue', 'green']
    :param ramp_time: Time to ramp up to target RGB.
    :return: Color sequence generator. This generator is infinite and continues to return the last value once the
    variable components are complete.
    """
    target_rgb = (0, 0, 0)

    for target in targets:
        target_rgb = webcolors.name_to_rgb(target)

        delta_rgb = [x/ramp_time for x in target_rgb]

        current_rgb = (0, 0, 0)
        while current_rgb < target_rgb:
            yield current_rgb
            current_rgb = tuple([floor(x+delta_rgb[i]) for i, x in enumerate(current_rgb)])
        yield target_rgb

    while True:
        yield target_rgb


def pulse_rgb(rgb, loop_time, frequency=1, decay_time=None):
    """ Pulse the RGB channels.

    :param rgb: The target RGB e.g. (255, 0, 0)
    :param loop_time: The time between each loop call e.g. 0.1s
    :param frequency: The frequency of the pulse (default 1Hz)
    :param decay_time: The amplitude decay time (s)

    :return: A generator.
    """

    for count in itertools.count():
        time = count * loop_time
        current = [_cosine(channel, frequency, time, decay_time)
                   for channel in rgb]
        yield tuple(current)


def _cosine(amplitude, frequency, time, decay_time):
    """ Light signal for a given channel. """

    decay = max((decay_time - time) / decay_time, 0.1) if decay_time else 1
    y = decay * amplitude * (cos(pi * 2 * time * frequency) + 1.0) / 2.0

    return ceil(y)
