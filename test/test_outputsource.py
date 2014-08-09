"""
test_outputsource.py - Unit tests for the outputsource module.

:author: Martin Norbury
"""
import mock
from nose.tools import eq_

from outputsource import Blink1Indicator


def constant_rgb(rgb):
    while True:
        yield rgb


class TestOutputSource(object):

    def __init__(self):
        self.mock_pattern = mock.MagicMock()
        self.mock_client = mock.MagicMock()
        self.output_source = Blink1Indicator(client=self.mock_client)

    def test_close_client_on_close(self):
        self.output_source.close()

        self.mock_client.close.assert_called_with()

    def test_turn_off_light_on_close(self):
        self.output_source.close()

        self.mock_client.off.assert_called_with()

    def test_sending_hardware_update(self):
        self.output_source.update_hardware(255, 255, 255)

        self.mock_client.fade_to_rgb(255, 255, 255)

    def test_sending_hardware_update_only_on_change(self):
        self.output_source.update_hardware(255, 255, 255)
        self.output_source.update_hardware(255, 255, 255)

        eq_(self.mock_client.fade_to_rgb.call_count, 1)