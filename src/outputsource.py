'''
Created on Jul 17, 2014

@author: mnorbury
'''
import webcolors
from blink1 import blink1

from pattern import pattern_factory

class Blink1Indicator(object):
    def __init__(self, client=blink1.Blink1(), pattern_factory=pattern_factory(0.1)):
        self._client = client
        self._last_data = None
        self._pattern = None
        self._pattern_factory = pattern_factory
    def update(self, data):

        if self._last_data != data:            
            target_rgb = webcolors.name_to_rgb(data['color'])
            frequency = data['activity']
            self._pattern = self._pattern_factory(target_rgb, frequency)

        rgb = next(self._pattern)

        self._client.fade_to_rgb(100, *rgb)

        self._last_data = data