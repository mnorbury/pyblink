"""
Created on Jul 17, 2014

@author: mnorbury
"""
from blink1 import blink1

import webcolors

import pattern


class Blink1Indicator(object):
    """ Blink1 LED output source. """

    def __init__(self, client=None):
        self._client = client if client else blink1.Blink1()

        self._last_rgb = ()

    def update_hardware(self, red, green, blue):
        """ Update the output source.

        :param red: Red value (0-255).
        :param green: Green value (0-255).
        :param blue: Blue value (0-255).
        """

        if self._last_rgb != (red, green, blue):
            self._client.fade_to_rgb(100, red, green, blue)

        self._last_rgb = (red, green, blue)

        return

    def close(self):
        """ Close down the output source. """

        self._client.off()
        self._client.close()
