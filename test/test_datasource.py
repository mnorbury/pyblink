"""
Test cases for the datasource classes.

:author: Martin Norbury (mnorbury@lcogt.net)
"""
import json
import itertools
import mock

from nose.tools import eq_
from mock import patch

import datasource


@patch('datasource.urlopen')
class TestDataSource(object):

    def __init__(self):
        self._mock_pattern_factory = mock.MagicMock()
        self._mock_hardware_source = mock.MagicMock()
        self.source = datasource.JenkinsDataSource('buildsba:8085', 0.1, 60,
                                                   pattern_factory=self._mock_pattern_factory,
                                                   hardware_source=self._mock_hardware_source)

    def test_blue_if_all_builds_are_blue(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['blue', ])

        data = self.source.update_data()

        eq_({'color': 'blue', 'activity': 0}, data)

    def test_yellow_if_all_builds_are_yellow(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['yellow', ])

        data = self.source.update_data()

        eq_({'color': 'yellow', 'activity': 0}, data)

    def test_red_if_all_builds_are_red(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['red', ])

        data = self.source.update_data()

        eq_({'color': 'red', 'activity': 0}, data)

    def test_red_if_any_build_is_red(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['red', 'blue'])

        data = self.source.update_data()

        eq_({'color': 'red', 'activity': 0}, data)

    def test_yellow_if_any_build_is_yellow_but_not_failed(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['yellow', 'blue'])

        data = self.source.update_data()

        eq_({'color': 'yellow', 'activity': 0}, data)

    def test_blue_with_activity_if_building(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['blue_anime', 'blue'])

        data = self.source.update_data()

        eq_({'color': 'blue', 'activity': 1}, data)

    def test_blue_with_activity_if_building(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['blue_anime', 'blue_anime'])

        data = self.source.update_data()

        eq_({'color': 'blue', 'activity': 2}, data)

    def test_pattern_is_created_first_time(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['red'])

        self.source.update_data()

        self._mock_pattern_factory.assert_called_once_with((255, 0, 0), 0.1, 0, 60)

    def test_pattern_is_only_created_first_time(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['red'])

        self.source.update_data()
        self.source.update_data()

        self._mock_pattern_factory.assert_called_once_with((255, 0, 0), 0.1, 0, 60)

    def test_pattern_is_recreated_if_data_changes(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['red'])
        self.source.update_data()

        _configure_mock(mock_urlopen, ['blue'])
        self.source.update_data()

        expected_call_1 = mock.call((255, 0, 0), 0.1, 0, 60)
        expected_call_2 = mock.call((0, 0, 255), 0.1, 0, 60)

        actual_calls = self._mock_pattern_factory.call_args_list

        eq_(actual_calls, [expected_call_1, expected_call_2])

    def test_iterating_through_pattern(self, mock_urlopen):
        _configure_mock(mock_urlopen, ['blue'])
        self._mock_pattern_factory.return_value = itertools.cycle([(255, 0, 0),
                                                                   (0, 255, 0),
                                                                   (0, 0, 255)])

        self.source.update_data()

        self.source.update_hardware()
        self.source.update_hardware()
        self.source.update_hardware()

        expected_calls = [mock.call(255, 0, 0),
                          mock.call(0, 255, 0),
                          mock.call(0, 0, 255)]

        eq_(self._mock_hardware_source.update_hardware.call_args_list, expected_calls)

    def test_closing_hardware(self, mock_urlopen):
        self.source.close()

        self._mock_hardware_source.close.assert_called_once()

def _configure_mock(mock_urlopen, colors):
    mock_connection = mock_urlopen()
    raw_data = {'jobs': [dict(color=color) for color in colors]}
    mock_connection.read.return_value = json.dumps(raw_data).encode()