"""
Main application controller.

:author: Martin Norbury (martin.norbury@gmail.com)
"""
import logging
_LOGGER = logging.getLogger(__name__)

import threading
import time
import signal


class Controller(threading.Thread):
    """ Main application controller. """

    def __init__(self, data_source, loop_period=0.1):
        super(Controller, self).__init__(daemon=True)

        self._data_source = data_source

        self._count = 0
        self._loop_period = loop_period
        self._running = True

        self._data = None

        self._register_exit_handler()

    def run(self, running_checker=None):

        running = running_checker if running_checker else lambda: self._running

        while running():
            if not self._count % 10:
                _LOGGER.debug('Get data')
                self._data_source.update_data()
            _LOGGER.debug('Update hardware')
            self._data_source.update_hardware()
            self._count += 1
            time.sleep(self._loop_period)

    def stop(self):
        self._running = False

    def _register_exit_handler(self):
        def signal_handler(signal, frame):
            self._data_source.close()
            self.stop()

        signal.signal(signal.SIGINT, signal_handler)
