"""
A command line utility for monitoring a Jenkins instance and reporting
the current state to a blink1 LED.

:author: Martin Norbury (martin.norbury@gmail.com)
"""
import logging

import webcolors

import outputsource

import pattern


_LOGGER = logging.getLogger(__name__)

from urllib.request import urlopen
import json

import itertools


class JenkinsDataSource(object):

    def __init__(self, build_host, loop_frequency, decay_period, hardware_source=None, pattern_factory=None):
        self._build_host = build_host
        self._loop_frequency = loop_frequency
        self._decay_period = decay_period
        self._hardware_source = hardware_source if hardware_source else outputsource.Blink1Indicator()
        self._pattern_factory = pattern_factory if pattern_factory else pattern.pulse_rgb

        self._last_state = None
        self._pattern = itertools.cycle([(0, 0, 0)])

    def update_data(self):

        jobs = self._read_jobs()
        activity = len([x for x in jobs if 'anime' in x['color']])
        color = self._aggregate(jobs)

        current_state = dict(color=color, activity=activity)
        if current_state != self._last_state:
            target_rgb = webcolors.name_to_rgb(color)
            self._pattern = self._pattern_factory(target_rgb,
                                                  self._loop_frequency,
                                                  activity,
                                                  self._decay_period)

        self._last_state = current_state

        return current_state

    def update_hardware(self):
        red, green, blue = next(self._pattern)

        self._hardware_source.update_hardware(red, green, blue)

        return

    def close(self):
        self._hardware_source.close()

        return

    def _read_jobs(self):
        """
        Read jobs list for Jenkins.

        returns the Jenkins job list.
        """

        build_url = 'http://{0}/api/json'.format(self._build_host)

        connection = urlopen(build_url)
        data = connection.read()
        connection.close()

        return json.loads(data.decode('utf-8'))['jobs']

    @staticmethod
    def _aggregate(jobs):
        """ Aggregate the Jenkins jobs into a single build state. """
        states = [x['color'] for x in jobs]

        cleaned_states = [x.replace('_anime', '') for x in states]

        result = 'grey'
        for state in ['red', 'yellow', 'blue']:
            if state in cleaned_states:
                result = state
                break

        return result
