'''
jenkins_monitor.py:
    A command line utility for monitoring a Jenkins instance and reporting
    the current state to a blink1 LED.

Author:
    Martin Norbury (martin.norbury@gmail.com)

July 2014
'''
from urllib import request
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_jobs(buildhost):
    '''
    Read jobs list for Jenkins.

    buildhost: The build host name.

    returns the Jenkins job list.
    '''

    buildurl = 'http://{0}/api/json'.format(buildhost)

    connection = request.urlopen(buildurl)
    data = connection.read()
    connection.close()

    return json.loads(data.decode('utf-8'))['jobs']

def aggregate(jobs):
    '''
    Aggregate the Jenkins jobs into a single build state.
    '''
    states = [x['color'] for x in jobs]

    cleaned_states = [x.replace('_anime', '') for x in states]

    result = 'grey'
    for state in ['red', 'yellow', 'blue']:
        if state in cleaned_states:
            result = state
            break

    return result

if __name__ == '__main__':
    import argparse
    import time
    from blink1 import blink1

    logging.info("Starting application")

    parser = argparse.ArgumentParser()
    parser.add_argument('build_url', help='Build URL')
    args = parser.parse_args()

    b1 = blink1.Blink1()
#    b1.off()

    jobs = read_jobs(args.build_url)
    state = aggregate(jobs)

    b1.fade_to_color(2000, state)
