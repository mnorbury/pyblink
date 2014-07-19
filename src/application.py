'''
Created on Jul 17, 2014

@author: mnorbury
'''
import logging
_LOGGER = logging.getLogger(__name__)

from controller import Controller
from datasource import JenkinsDataSource
from outputsource import Blink1Indicator
import pattern
import signal

if __name__ == '__main__':

    # Configurable inputs
    buildhost = 'buildsba:8085'
    loop_period = 0.1
    decay_period = 30
    level = getattr(logging, 'debug'.upper())
    logging.basicConfig(level=level, format='%(asctime)-15s %(message)s')

    # Build controller
    pattern_factory = pattern.pattern_factory(loop_period, decay_period)
    input_source = JenkinsDataSource(buildhost)
    output_source = Blink1Indicator(pattern_factory)
    controller = Controller(input_source, output_source)

    # Attach ctrl-c handler
    def signal_handler(signal, frame):
        output_source.close()
        controller.stop()
    signal.signal(signal.SIGINT, signal_handler)

    # Start controller
    controller.start()
    controller.join()
