"""
Test cases for the datasource classes.

:author: Martin Norbury (mnorbury@lcogt.net)
"""
import json

from nose.tools import eq_
from mock import patch

import datasource


class TestDataSource(object):

    def __init__(self):
        self.source = datasource.JenkinsDataSource('buildsba:8085')

    @patch('datasource.urlopen')
    def test_blue_if_all_builds_are_blue(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['blue', ])

        data = self.source.retrieve_data()

        eq_({'color': 'blue', 'activity': 0}, data)

    @patch('datasource.urlopen')
    def test_yellow_if_all_builds_are_yellow(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['yellow', ])

        data = self.source.retrieve_data()

        eq_({'color': 'yellow', 'activity': 0}, data)

    @patch('datasource.urlopen')
    def test_red_if_all_builds_are_red(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['red', ])

        data = self.source.retrieve_data()

        eq_({'color': 'red', 'activity': 0}, data)

    @patch('datasource.urlopen')
    def test_red_if_any_build_is_red(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['red', 'blue'])

        data = self.source.retrieve_data()

        eq_({'color': 'red', 'activity': 0}, data)

    @patch('datasource.urlopen')
    def test_yellow_if_any_build_is_yellow_but_not_failed(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['yellow', 'blue'])

        data = self.source.retrieve_data()

        eq_({'color': 'yellow', 'activity': 0}, data)

    @patch('datasource.urlopen')
    def test_blue_with_activity_if_building(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['blue_anime', 'blue'])

        data = self.source.retrieve_data()

        eq_({'color': 'blue', 'activity': 1}, data)

    @patch('datasource.urlopen')
    def test_blue_with_activity_if_building(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['blue_anime', 'blue_anime'])

        data = self.source.retrieve_data()

        eq_({'color': 'blue', 'activity': 2}, data)


def _configure_mock(mock_urlopen, colors):
    mock_connection = mock_urlopen()
    raw_data = {'jobs': [dict(color=color) for color in colors]}
    mock_connection.read.return_value = json.dumps(raw_data).encode()