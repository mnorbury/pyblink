'''
Created on Jul 17, 2014

@author: mnorbury
'''
import argparse
import time
import signal
import sys

import outputsource
import pattern

def pyblink_test():
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', default='green', help='Color to display')
    parser.add_argument('--activity', default=1, type=int, help='Activity value')
    parser.add_argument('--loop_time', default=0.1, type=float, help='Loop Time (s)')
    parser.add_argument('--decay_time', default=600, type=float, help='Decay Time (s)')
    args = parser.parse_args()

    factory = pattern.pattern_factory(args.loop_time, args.decay_time)
    blink = outputsource.Blink1Indicator(factory)

    # Attach ctrl-c handler
    def signal_handler(signal, frame):
        blink.close()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        blink.update(args.__dict__)
        time.sleep(args.loop_time)
