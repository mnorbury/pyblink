'''
test_outputsource.py - Unit tests for the outputsource module.

:author: Martin Norbury
'''
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
        self.output_source = Blink1Indicator(self.mock_pattern,
                                             self.mock_client)

    def test_close_client_on_close(self):
        self.output_source.close()

        self.mock_client.close.assert_called_with()

    def test_turn_off_light_on_close(self):
        self.output_source.close()

        self.mock_client.off.assert_called_with()

    def test_creating_new_pattern(self):
        self.output_source.update(dict(color='red', activity=1))

        self.mock_pattern.assert_called_with((255,0,0),1)

    def test_only_create_pattern_first_time(self):
        self.output_source.update(dict(color='red', activity=1))
        self.output_source.update(dict(color='red', activity=1))

        self.mock_pattern.assert_called_once_with((255,0,0),1)

    def test_create_pattern_if_color_changes(self):
        self.output_source.update(dict(color='red', activity=1))
        self.mock_pattern.assert_called_with((255,0,0),1)

        self.output_source.update(dict(color='yellow', activity=1))
        self.mock_pattern.assert_called_with((255,255,0),1)


    def test_send_fade_request_to_client(self):
        self.mock_pattern.return_value = constant_rgb((255,0,0))

        self.output_source.update(dict(color='red', activity=1))

        self.mock_client.fade_to_rgb(100,(255,0,0))
