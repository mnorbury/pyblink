from math import cos, pi


def pattern_factory(loop_time, decay_time):

    def _pulse_signal(amplitude, frequency, time):
        decay = max((decay_time - time)/decay_time, 0.1) if decay_time else 1

        y = decay * amplitude * (cos(pi * 2 * time * frequency) + 1.0)

        return y

    def pulse_rgb(target, frequency=1):

        count = 0

        amplitude = [int(x / 2.0) for x in target]

        while True:
            current = [int(_pulse_signal(x, frequency, count * loop_time))
                       for x in amplitude]
            yield tuple(current)
            count += 1

    return pulse_rgb
