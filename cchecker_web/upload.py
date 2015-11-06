#!/usr/bin/env python
'''
Compliance Checker Web
~~~~~~~~~~~~~~~~~~~~~~

'''

from cchecker_web import cchecker_web, login_required
from cchecker_web.processing import compliance_check
from cchecker_web.user import UserAppStore
from flask import request, jsonify, session
from flask import current_app as app
from hashlib import sha1
from datetime import datetime
import base64
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
@login_required
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
    user_token = session['user_token']
    user_store = UserAppStore(user_token)
    user = user_store.read(user_id='self')
    user_id = user['user_id']

    for filename in files:
        file_object = files[filename]
        if not allowed_file(file_object.filename):
            continue
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 
                                user_id,
                                base64.b64encode(file_object.filename))
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        file_object.save(filepath)
        job_id = get_job_id(filepath)
        app.queue.enqueue_call(func=compliance_check, args=(job_id, filepath, checker))
        successful.append(file_object.filename)
        break
    else:
        return jsonify(error='upload_failed', message='Upload failed'), 400

    return jsonify(message='Upload successful', job_id=job_id, files=successful)
            
