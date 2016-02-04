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
    job_result = json.loads(job_result)
    if 'error' in job_result:
        return jsonify(job_result), 400
    return jsonify(job_result), 200

@api.route('/api/config')
def show_config():
    size_limit = app.config.get('MAX_CONTENT_LENGTH')
    return jsonify(size_limit=size_limit)
