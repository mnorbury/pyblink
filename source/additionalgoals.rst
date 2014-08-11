Additional Goals
================

* **Python 3.x:** Since the Blink api uses Python3.x, this will be an opportunity to use newer versions of Python.
* **Generators:** The Blink patterns can easily be produced using generators e.g. the pulse pattern generator::

    def pulse_rgb(rgb, loop_time, frequency=1, decay_time=None):
        """ Pulse the RGB channels.

        :param rgb: The target RGB e.g. (255, 0, 0)
        :param loop_time: The time between each loop call e.g. 0.1s
        :param frequency: The frequency of the pulse (default 1Hz)
        :param decay_time: The amplitude decay time (s)

        :return: A generator.
        """

        for count in itertools.count():
            time = count * loop_time
            current = [_cosine(channel, frequency, time, decay_time)
                       for channel in rgb]
            yield tuple(current)


* **Sphinx:** Document the project using this popular tool (http://sphinx-doc.org/).
* **Github Pages:** Host custom project documentation on github (https://pages.github.com/).
* **Travis CI:** Build and test using cloud-based CI server (https://travis-ci.org/).
* **Coveralls:** Generate test coverage using this cloud-based service (https://coveralls.io/).
