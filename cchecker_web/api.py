#!/usr/bin/env python
'''
cchecker_web/api.py
'''

from cchecker_web import cchecker_web as api
from cchecker_web.upload import get_job_id
from cchecker_web.processing import compliance_check
from flask import request, redirect, jsonify, current_app as app
from compliance_checker.runner import CheckSuite
import json
import time


@api.route('/api/job/<string:job_id>')
def show_job(job_id):
    job_result = app.redis.get('processing:job:%s' % job_id)
    if job_result is None:
        return jsonify({}), 404
    if isinstance(job_result, str):
        job_result = json.loads(job_result)
    else:
        job_result = json.loads(job_result.decode('utf-8'))
    if 'error' in job_result:
        return jsonify(job_result), 400
    return jsonify(job_result), 200


@api.route('/api/config')
def show_config():
    size_limit = app.config.get('MAX_CONTENT_LENGTH')
    return jsonify(size_limit=size_limit)


@api.route('/api/tests', methods=['GET'])
def get_tests():
    '''
    Returns the listing of tests for compliance checker
    '''
    tests = populate_tests()
    return json.dumps(tests), 200, {"Content-Type": "application/json"}


@api.route('/api/run')
def execute_job():
    '''
    'Rest' endpoint for running compliance checker. Only accepts DAP urls.
    '''
    # Get parameters
    report_format = request.args.get('report_format', 'json')
    test = request.args.get('test', None)
    url = request.args.get('url', None)

    # Check report formats
    accepted_formats = ['json', 'html']
    if report_format not in accepted_formats:
        err_msg = ("Report format '{0}' not available. "
                   "Please choose from {1}".format(report_format, accepted_formats))
        return jsonify({'Error': err_msg}), 400

    # Check the tests
    tests = populate_tests()
    test_ids = [t['id'] for t in tests]
    if test not in test_ids:
        err_msg = ("Test '{0}' not available. "
                   "Please choose from {1}".format(test, test_ids))
        return jsonify({'Error': err_msg}), 400

    # Check required fields and process
    required_fields = [test, url]
    if all(required_fields):
        # Kick off the job
        job_id = get_job_id(url)
        app.queue.enqueue_call(func=compliance_check, args=(job_id, url, test))
        job_result = None
        timeout = 20  # secs

        # Now we check to see if processing is done
        for tries in xrange(timeout):
            time.sleep(1)
            job_result = app.redis.get('processing:job:%s' % job_id)

            if job_result is None:
                # Not done yet, try again
                continue

            if 'error' in job_result:
                return jsonify(job_result), 500

            if isinstance(job_result, str):
                job_result = json.loads(job_result)
            else:
                job_result = json.loads(job_result.decode('utf-8'))

            # Check the report format for how to return the results
            if report_format == 'html':
                return redirect('/report/' + job_id)
            else:
                return jsonify(job_result), 200

        return jsonify({'Error': 'Job timed out'}), 500
    else:
        return jsonify({'Error': 'Incorrect Inputs. Please provide a url and a test'}), 400


def populate_tests():
    '''
    Returns the listing of tests for compliance checker
    '''
    tests = []
    keys = []
    for test_name, checker in CheckSuite.checkers.items():
        spec = getattr(checker, '_cc_spec', test_name)
        pretty_spec = prettify(spec)
        version = getattr(checker, '_cc_spec_version', '')
        description = getattr(checker, '_cc_description', '')
        key = '{} {}'.format(spec, version)
        if key in keys:
            continue
        keys.append(key)
        tests.append({
            "id": test_name,
            "version": version,
            "name": pretty_spec,
            "description": description
        })
    tests = sorted(tests, key=lambda x: x['name'])
    return tests


def prettify(ugly):
    '''
    Returns a prettier string

    :param str ugly: An ugly string
    '''
    pretty = ugly.replace('-', ' ')
    pretty = pretty.title()
    buf = []
    for token in pretty.split(' '):
        if token.upper() in ('IOOS', 'CF', 'ACDD', 'NCEI'):
            buf.append(token.upper())
        elif token.lower() == 'timeseriesprofile':
            buf.append('Timeseries Profile')
        elif token.lower() == 'incompletetime':
            buf.append('Incomplete Time')
        elif token.lower() == 'incompletedepth':
            buf.append('Incomplete Depth')
        elif token.lower() == 'orthtime':
            buf.append("Orthogonal Time")
        elif token.lower() == "gliderdac":
            buf.append("Glider DAC")
        elif token.lower() == 'trajectoryprofile':
            buf.append('Trajectory Profile')
        else:
            buf.append(token)

    return ' '.join(buf)
