"""
A command line utility for monitoring a Jenkins instance and reporting
the current state to a blink1 LED.

:author: Martin Norbury (martin.norbury@gmail.com)
"""
import logging
_LOGGER = logging.getLogger(__name__)

from urllib.request import urlopen
import json


class JenkinsDataSource(object):

    def __init__(self, build_host):
        self._build_host = build_host

    def retrieve_data(self):
        """ Return build data in the form of:-

            {
               'color' : 'red',
               'activity' : 1,
            }
        """

        jobs = self._read_jobs()
        activity = len([x for x in jobs if 'anime' in x['color']])
        color = self._aggregate(jobs)

        return dict(color=color, activity=activity)

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
