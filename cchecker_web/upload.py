#!/usr/bin/env python
'''
Compliance Checker Web
~~~~~~~~~~~~~~~~~~~~~~

'''

from cchecker_web import cchecker_web
from cchecker_web.processing import compliance_check
from flask import request, jsonify, session
from flask import current_app as app
from hashlib import sha1
from datetime import datetime
import base64
import os
import subprocess

ALLOWED_FILENAMES = ['.nc', '.nc3', '.nc4', '.netcdf', '.netcdf3', '.netcdf4', '.cdl']


def allowed_file(filename):
    if os.path.splitext(filename)[-1] in ALLOWED_FILENAMES:
        return True
    return False


def get_job_id(filepath):
    datestr = datetime.utcnow().isoformat()
    return sha1((filepath + datestr).encode('utf-8')).hexdigest()


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
    return jsonify(message='Job Created', job_id=job_id)


def check_files(files, checker):
    successful = []

    for filename in files:
        file_object = files[filename]
        if not allowed_file(file_object.filename):
            continue
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                encode(file_object.filename))
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        file_object.save(filepath)

        # Check for a metadata .cdl file and if so, return new filepath
        try:
            filepath = check_for_cdl(file_object.filename, filepath)
        except Exception as e:
            return jsonify(error='upload_failed', message='Upload failed: ' + str(e)), 400

        job_id = get_job_id(filepath)
        app.queue.enqueue_call(func=compliance_check, args=(job_id, filepath, checker))
        successful.append(file_object.filename)
        break
    else:
        return jsonify(error='upload_failed', message='Upload failed'), 400

    return jsonify(message='Upload successful. Please wait a moment while we process the file...', job_id=job_id, files=successful)


def generate_dataset(nc_path, cdl_path):
    subprocess.call(['ncgen', '-o', nc_path, cdl_path])


def check_for_cdl(filename, filepath):
    # Check for a metadata .cdl file
    if os.path.splitext(filename)[-1] == '.cdl':
        nc_file = filename.replace('.cdl', '.nc')
        nc_path = os.path.join(app.config['UPLOAD_FOLDER'],
                               encode(nc_file))
        filepath = update_cdl_dimensions(filepath)
        generate_dataset(nc_path, filepath)
        filepath = nc_path
    return filepath


def update_cdl_dimensions(filename):
    '''
    Rewrite the cdl file to make all dimensions size 1
    '''
    transform = False
    data = []
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:  # End of file
                break
            if 'variables:' in line:
                transform = False
            elif transform:  # These lines are dimensions. They should be size 1
                prefix = line.split('=')[0]
                line = prefix + '= 1 ;\n'
            elif 'dimensions:' in line:
                # This is where we start transforming dimensions
                transform = True
            data.append(line)
    # Re write the file
    with open(filename, 'w') as f:
        f.write(''.join(data))
    return filename


def encode(s):
    return base64.b64encode(s.encode('utf-8')).decode('ascii')
