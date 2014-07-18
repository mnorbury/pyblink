'''
Created on Jul 17, 2014

@author: mnorbury
'''
import webcolors
from blink1 import blink1


class Blink1Indicator(object):

    def __init__(self, pattern_factory, client=blink1.Blink1()):
        self._pattern_factory = pattern_factory
        self._client = client
        self._last_data = None
        self._pattern = None

    def update(self, data):

        if self._last_data != data:
            target_rgb = webcolors.name_to_rgb(data['color'])
            frequency = data['activity']
            self._pattern = self._pattern_factory(target_rgb, frequency)

        rgb = next(self._pattern)

        self._client.fade_to_rgb(100, *rgb)

        self._last_data = data

    def close(self):
        self._client.off()
        self._client.close()
