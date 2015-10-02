#!/usr/bin/env python
'''
Compliance Checker Web
~~~~~~~~~~~~~~~~~~~~~~

'''

from cchecker_web import cchecker_web
from cchecker_web.processing import compliance_check
from flask import request, jsonify
from flask import current_app as app
from hashlib import sha1
from datetime import datetime
import os

def allowed_file(filename):
    return True

def get_job_id(filepath):
    datestr = datetime.utcnow().isoformat()
    return sha1(filepath + datestr).hexdigest()

@cchecker_web.route('/upload', methods=['POST'])
def upload_dataset():
    successful = []
    if not request.files:
        return jsonify(error='UploadError', message='No files found')
    for filename in request.files:
        file_object = request.files[filename]
        if allowed_file(filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_object.filename)
            file_object.save(filepath)
            job_id = get_job_id(filepath)
            app.queue.enqueue(compliance_check, job_id, filepath, 'gliderdac')
            successful.append(file_object.filename)
            break
    if successful:
        return jsonify(message='Upload successful', job_id=job_id, files=successful)
            
    return jsonify(error='upload_failed', message='Upload failed'), 400

