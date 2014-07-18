import math


def pattern_factory(loop_time):

    def _pulse_signal(x, frequency, count):
        y = x * 0.5 * \
            (math.cos(math.pi * 2 * count * loop_time * frequency) + 1.0)
        return y

    def pulse_rgb(target, frequency=1):

        count = 0

        amplitude = [int(x / 2.0) for x in target]

        while True:
            current = [int(_pulse_signal(x, frequency, count))
                       for x in amplitude]
            yield tuple(current)
            count += 1

    return pulse_rgb
