"""
The main application file.

:author: mnorbury
"""
import logging
import signal
import argparse

_LOGGER = logging.getLogger(__name__)

from controller import Controller
from datasource import JenkinsDataSource
from outputsource import Blink1Indicator


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Jenkins build monitor.")
    parser.add_argument('-build_host', default='buildsba:8085')
    parser.add_argument('-loop_period', default=0.1)
    parser.add_argument('-decay_period', default=30)
    parser.add_argument('-log_level', default='info')
    arguments = parser.parse_args()

    # Configurable inputs
    logging.basicConfig(level=(getattr(logging, arguments.log_level.upper())), format='%(asctime)-15s %(message)s')

    # Build controller
    input_source = JenkinsDataSource(arguments.build_host)
    output_source = Blink1Indicator(arguments.loop_period)
    controller = Controller(input_source, output_source)

    # Attach ctrl-c handler
    def signal_handler(signal, frame):
        output_source.close()
        controller.stop()
    signal.signal(signal.SIGINT, signal_handler)

    # Start controller
    controller.start()
    controller.join()
