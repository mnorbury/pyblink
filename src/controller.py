'''
Created on Jul 17, 2014

@author: mnorbury
'''
import logging
_LOGGER = logging.getLogger(__name__)

import threading
import time

class Controller(threading.Thread):
    ''' Main application controller. '''

    def __init__(self, datasource, hardware):
        super(Controller, self).__init__(daemon=True)

        self._datasource = datasource
        self._hardware = hardware

        self._count = 0
        self._loop_period = 0.1
        self._running = True

        self._data = None

    def run(self):
        while self._running:
            if not self._count % 10:
                _LOGGER.debug('Get data')
                self._data = self._datasource.retrieve_data()
            _LOGGER.debug('Update hardware')
            self._hardware.update(self._data)
            self._count += 1
            time.sleep(self._loop_period)

    def stop(self):
        self._running = False

