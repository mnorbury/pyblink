"""
Module containing script entry points.

:author: mnorbury
"""
import argparse
import time
import sys
import signal

import outputsource


def pyblink_test():
    """ Simple command line utility for testing the blink(1) """

    parser = argparse.ArgumentParser()
    parser.add_argument('--color', default='green', help='Color to display')
    parser.add_argument('--activity', default=1, type=int, help='Activity value')
    parser.add_argument('--loop_time', default=0.1, type=float, help='Loop Time (s)')
    parser.add_argument('--decay_time', default=600, type=float, help='Decay Time (s)')
    args = parser.parse_args()

    blink = outputsource.Blink1Indicator(args.loop_time)

    # Attach ctrl-c handler
    def signal_handler(signal, frame):
        blink.close()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        blink.update(dict(color=args.color,activity=args.activity))
        time.sleep(args.loop_time)