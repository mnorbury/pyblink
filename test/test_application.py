import mock

import application


@mock.patch('application.Controller')
@mock.patch('application.JenkinsDataSource')
@mock.patch('application.Blink1Indicator')
class TestApplication(object):

    def __init__(self):
        self._loop_time = 0.1
        self._host_name = 'buildsba:8085'

    def test_create_input_data(self, mock_blink, mock_input, mock_controller):
        application.main([])

        mock_input.assert_called_with(self._host_name)

    def test_create_output_source(self, mock_blink, mock_input, mock_controller):
        application.main([])

        mock_blink.assert_called_with(self._loop_time)

    def test_create_output_source_with_custom_loop_time(self, mock_blink, mock_input, mock_controller):
        custom_loop_time = 0.5

        application.main(['-loop_period', '0.5'])

        mock_blink.assert_called_with(custom_loop_time)

    def test_create_controller(self, mock_blink, mock_input, mock_controller):
        application.main([])

        mock_controller.assert_called_with(mock_input(), mock_blink())

    def test_starting_controller(self, mock_blink, mock_input, mock_controller):
        application.main([])

        mock_controller().start.assert_called_with()