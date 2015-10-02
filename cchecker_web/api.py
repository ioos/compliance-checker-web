#!/usr/bin/env python
'''
cchecker_web/api.py
'''

from cchecker_web import cchecker_web as api
from flask import jsonify, current_app as app
import json

@api.route('/api/job/<string:job_id>')
def show_job(job_id):
    job_result = app.redis.get('processing:job:%s' % job_id)
    if job_result is None:
        return jsonify({}), 404
    return job_result or '{}', 200, {'Content-Type':'application/json;charset=utf8'}
    
