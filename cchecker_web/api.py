#!/usr/bin/env python
'''
cchecker_web/api.py
'''

from cchecker_web import cchecker_web as api
from flask import jsonify, current_app as app
from compliance_checker.runner import CheckSuite
import json

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

    return json.dumps(tests), 200, {"Content-Type": "application/json"}


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

