import mock

import scripts


class TestScripts(object):

    @mock.patch('scripts._run_monitor_jenkins')
    def test_default_arguments(self, mock_jenkins_monitor):
        scripts.monitor_jenkins(['pyblink'])

        mock_jenkins_monitor.assert_called_with('buildsba:8085', 0.1, 60)

    @mock.patch('scripts._run_monitor_jenkins')
    def test_build_host_argument(self, mock_jenkins_monitor):
        scripts.monitor_jenkins(['pyblink', '-build_host', 'localhost'])

        mock_jenkins_monitor.assert_called_with('localhost', 0.1, 60)

    @mock.patch('scripts._run_monitor_jenkins')
    def test_loop_period_argument(self, mock_jenkins_monitor):
        scripts.monitor_jenkins(['pyblink', '-loop_period', '0.5'])

        mock_jenkins_monitor.assert_called_with('buildsba:8085', 0.5, 60)

    @mock.patch('scripts._run_monitor_jenkins')
    def test_decay_time_argument(self, mock_jenkins_monitor):
        scripts.monitor_jenkins(['pyblink', '-decay_period', '30'])

        mock_jenkins_monitor.assert_called_with('buildsba:8085', 0.1, 30)

    @mock.patch('scripts._create_controller')
    def test_creating_controller(self, mock_create_controller):
        scripts._run_monitor_jenkins(1, 2, 3)

        mock_create_controller.assert_called_with(1, 2, 3)

    @mock.patch('scripts._create_controller')
    def test_starting_controller(self, mock_create_controller):
        mock_controller = mock_create_controller()

        scripts._run_monitor_jenkins(1, 2, 3)

        mock_controller.start.assert_called_with()

    @mock.patch('scripts._create_controller')
    def test_thread_join(self, mock_create_controller):
        mock_controller = mock_create_controller()

        scripts._run_monitor_jenkins(1, 2, 3)

        mock_controller.join.assert_called_with()