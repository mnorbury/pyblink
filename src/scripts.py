"""
Module containing script entry points.

:author: mnorbury
"""
import argparse
import logging

from controller import Controller
from datasource import JenkinsDataSource
import outputsource
import sys


def monitor_jenkins(arguments=None):
    arguments = arguments if arguments else sys.argv

    parser = argparse.ArgumentParser(description="Jenkins build monitor.")
    parser.add_argument('-build_host', default='buildsba:8085')
    parser.add_argument('-loop_period', type=float, default=0.1)
    parser.add_argument('-decay_period', type=float, default=60)
    parser.add_argument('-log_level', default='info')
    arguments = parser.parse_args(arguments[1:])

    logging.basicConfig(level=(getattr(logging, arguments.log_level.upper())), format='%(asctime)-15s %(message)s')

    _run_monitor_jenkins(arguments.build_host,
                         arguments.loop_period,
                         arguments.decay_period,)

    return


def _run_monitor_jenkins(build_host, loop_period, decay_period):

    controller = _create_controller(build_host, loop_period, decay_period)
    controller.start()
    controller.join()

    return


def _create_controller(build_host, loop_period, decay_period):
    input_source = JenkinsDataSource(build_host, loop_period, decay_period)
    controller = Controller(input_source)

    return controller

