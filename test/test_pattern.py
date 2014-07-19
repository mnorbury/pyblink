'''
test_pattern.py - Test cases for the pattern module.

:author: Martin Norbury
'''
from nose.tools import with_setup, eq_

from pattern import pulse_rgb

class TestPattern(object):

    def __init__(self):
        self.pulse_generator = pulse_rgb((255,0,0), 0.1)

    def test_first_value_is_target(self):
        result = next(self.pulse_generator)

        eq_((255,0,0), result)

    def test_mid_phase_is_zero(self):
        for i in range(6):
            result = next(self.pulse_generator)

        eq_((0,0,0), result)

    def test_full_phase_us_target(self):
        for i in range(11):
            result = next(self.pulse_generator)

        eq_((255,0,0), result)
