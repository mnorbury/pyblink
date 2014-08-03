"""
The main application file.

:author: mnorbury
"""
import logging
import signal
import argparse
import sys

_LOGGER = logging.getLogger(__name__)

from controller import Controller
from datasource import JenkinsDataSource
from outputsource import Blink1Indicator


def main(argv):
    arguments = _read_command_line(argv)

    logging.basicConfig(level=(getattr(logging, arguments.log_level.upper())), format='%(asctime)-15s %(message)s')

    controller, output_source = _create_controller(arguments)

    _register_exit_handler(controller, output_source)

    controller.start()
    controller.join()


def _read_command_line(argv):
    parser = argparse.ArgumentParser(description="Jenkins build monitor.")
    parser.add_argument('-build_host', default='buildsba:8085')
    parser.add_argument('-loop_period', type=float, default=0.1)
    parser.add_argument('-decay_period', default=30)
    parser.add_argument('-log_level', default='info')
    arguments = parser.parse_args(argv)
    return arguments


def _create_controller(arguments):
    input_source = JenkinsDataSource(arguments.build_host)
    output_source = Blink1Indicator(arguments.loop_period)
    controller = Controller(input_source, output_source)
    return controller, output_source


def _register_exit_handler(controller, output_source):
    def signal_handler(signal, frame):
        output_source.close()
        controller.stop()

    signal.signal(signal.SIGINT, signal_handler)

    return

if __name__ == '__main__':
    main(sys.argv[1:])