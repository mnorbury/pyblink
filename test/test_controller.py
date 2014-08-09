"""
Test cases for the controller module.

:author: Martin Norbury (mnorbury@lcogt.net)
"""

import mock
from nose.tools import eq_
from controller import Controller


@mock.patch('controller.time')
class TestController(object):

    def __init__(self):
        self.data_source = mock.MagicMock()
        self.hardware = mock.MagicMock()
        self.controller = Controller(self.data_source)
        self._count = 0
        self._complete = 1

    def test_retrieve_data(self, mock_time):
        running_function = self._make_is_running(1)

        self.controller.run(running_function)

        eq_(self.data_source.update_data.call_count, 1)

    def test_retrieve_data_two_times(self, mock_time):
        running_function = self._make_is_running(20)

        self.controller.run(running_function)

        eq_(self.data_source.update_data.call_count, 2)

    def test_update_hardware_each_loop(self, mock_time):
        running_function = self._make_is_running(20)

        self.controller.run(running_function)

        eq_(self.data_source.update_hardware.call_count, 20)

    def test_update_hardware(self, mock_time):
        running_function = self._make_is_running(1)

        self.controller.run(running_function)

        self.data_source.update_hardware.assert_called_with()

    def test_set_running_flag(self, mock_time):
        eq_(self.controller._running, True)

        self.controller.stop()

        eq_(self.controller._running, False)

    def _make_is_running(self, complete):
        def _is_running_function():
            is_running = not (self._count == complete)
            self._count += 1
            return is_running
        return _is_running_function