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

ALLOWED_FILENAMES = ['.nc', '.nc3', '.nc4', '.netcdf', '.netcdf3', '.netcdf4']

def allowed_file(filename):
    print filename
    if filename.endswith('.nc'):
        return True
    return False

def get_job_id(filepath):
    datestr = datetime.utcnow().isoformat()
    return sha1(filepath + datestr).hexdigest()

@cchecker_web.route('/upload', methods=['POST'])
def upload_dataset():
    url = request.form.get('url')
    checker = request.form.get('checker')
    if not checker:
        return jsonify(error='ValueError', message='Invalid checker'), 400
    if url:
        return check_url(url, checker)
    elif request.files:
        return check_files(request.files, checker)
    return jsonify(error='UploadError', message='No files found')


def check_url(url, checker):
    job_id = get_job_id(url)
    app.queue.enqueue_call(func=compliance_check, args=(job_id, url, checker))
    return jsonify(message='Check successful', job_id=job_id)


def check_files(files, checker):
    successful = []
    for filename in files:
        file_object = files[filename]
        if allowed_file(file_object.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_object.filename)
            file_object.save(filepath)
            job_id = get_job_id(filepath)
            app.queue.enqueue_call(func=compliance_check, args=(job_id, filepath, checker))
            successful.append(file_object.filename)
            break
    if successful:
        return jsonify(message='Upload successful', job_id=job_id, files=successful)
            
    return jsonify(error='upload_failed', message='Upload failed'), 400
