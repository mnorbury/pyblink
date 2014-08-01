"""
Created on Jul 17, 2014

@author: mnorbury
"""
from blink1 import blink1

import webcolors

import pattern


class Blink1Indicator(object):
    """ Blink1 LED output source. """

    def __init__(self, loop_frequency, pattern_factory=pattern.pulse_rgb, client=None):
        """
        :param pattern_factory: Function for creating pattern values.
        """
        self._pattern_factory = pattern_factory
        self._client = client if client else blink1.Blink1()
        self._loop_frequency = loop_frequency
        self._last_data = None
        self._pattern = None

    def update(self, data):
        """ Update the output source.

        :param data: Data to use to update the output source.
        """

        if self._last_data != data:
            target_rgb = webcolors.name_to_rgb(data['color'])
            frequency = data['activity']
            self._pattern = self._pattern_factory(target_rgb, self._loop_frequency, frequency, 60)

        rgb = next(self._pattern)

        self._client.fade_to_rgb(100, *rgb)

        self._last_data = data

    def close(self):
        """ Close down the output source. """

        self._client.off()
        self._client.close()
