import mock
import nose

import scripts


@mock.patch('scripts.time')
@mock.patch('scripts.outputsource.Blink1Indicator')
class TestScripts(object):

    def __init__(self):
        self._count = 0

        self._loop_time = 0.1

    def test_create_blink_indicator(self, mock_blink, mock_time):
        scripts._run_pyblink_test([], self._running)

        mock_blink.assert_called_with(self._loop_time)

    def test_call_to_blink_update_with_defaults(self, mock_blink, mock_time):
        scripts._run_pyblink_test([], self._running)

        mock_blink().update.assert_called_with(dict(color='green', activity=1))

    def test_call_to_blink_update_with_custom_color(self, mock_blink, mock_time):
        scripts._run_pyblink_test(['--color', 'red', '--activity', '2'], self._running)

        mock_blink().update.assert_called_with(dict(color='red', activity=2))


    def _running(self):
        self._count += 1
        return not self._count == 2