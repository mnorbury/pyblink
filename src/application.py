'''
Created on Jul 17, 2014

@author: mnorbury
'''
import threading
import time

class Controller(threading.Thread):
    def __init__(self, datasource, hardware):
        super(Controller, self).__init__()

        self._datasource = datasource
        self._hardware = hardware

        self._count = 0
        self._loop_period = 0.1
        self._running = True

        self._data = None

    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            if not self._count % 10:
                print('Get data')
                self._data = self._datasource.retrieve_data()
            print('Update hardware')
            self._hardware.update(self._data)
            self._count += 1
            time.sleep(self._loop_period)

if __name__ == '__main__':
    from datasource import JenkinsDataSource
    from outputsource import Blink1Indicator
    import pattern

    buildhost = 'buildsba:8085'

    pattern_factory = pattern.pattern_factory(0.1, 600)
    controller = Controller(JenkinsDataSource(buildhost), Blink1Indicator(pattern_factory))
    controller.start()
