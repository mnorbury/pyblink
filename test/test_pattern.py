"""
test_pattern.py - Test cases for the pattern module.

:author: Martin Norbury (martin.norbury@gmail.com)
"""
import itertools
from nose.tools import eq_

from pattern import pulse_rgb, color_sequence


class TestPulsePattern(object):

    def __init__(self):
        self.pulse_generator = pulse_rgb((255, 0, 0), 0.1)

    def test_first_value_is_target(self):
        result = next(self.pulse_generator)

        eq_((255, 0, 0), result)

    def test_mid_phase_is_zero(self):
        result = None
        for i in range(6):
            result = next(self.pulse_generator)

        eq_((0, 0, 0), result)

    def test_full_phase_is_target(self):
        result = None
        for i in range(11):
            result = next(self.pulse_generator)

        eq_((255, 0, 0), result)


class TestSequencePattern(object):

    def __init__(self):
        self._sequence = color_sequence(['red'])

    def test_first_value(self):
        value = next(self._sequence)

        eq_(value, (0, 0, 0))

    def test_second_value(self):
        next(self._sequence)
        value = next(self._sequence)

        eq_(value, (25, 0, 0))

    def test_finish_at_target(self):
        values = list(itertools.islice(self._sequence, 100))

        eq_(values[-1], (255, 0, 0))