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
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], job_id)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    app.queue.enqueue_call(func=compliance_check, args=(job_id, url, checker, filepath))
    return jsonify(message='Job Created', job_id=job_id)


def check_files(files, checker):
    successful = []

    for filename in files:
        file_object = files[filename]
        if not allowed_file(file_object.filename):
            continue
        job_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                encode(file_object.filename))
        job_id = get_job_id(job_path)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                job_id,
                                encode(file_object.filename))

        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        file_object.save(filepath)

        # Check for a metadata .cdl file and if so, return new filepath
        try:
            filepath = check_for_cdl(file_object.filename, filepath)
        except Exception as e:
            return jsonify(error='upload_failed', message='Upload failed: ' + str(e)), 400

        app.queue.enqueue_call(func=compliance_check, args=(job_id, filepath, checker))
        successful.append(file_object.filename)
        break
    else:
        return jsonify(error='upload_failed', message='Upload failed'), 400

    return jsonify(message='Upload successful. Please wait a moment while we process the file...', job_id=job_id, files=successful)


def generate_dataset(nc_path, cdl_path):
    '''
    Use ncgen to generate a netCDF file from a .cdl file

    :param str nc_path: Absolute path to netCDF file that will be generated
    :param str cdl_path: Absolute path to cdl file that is used to generate netCDF file
    '''
    subprocess.call(['ncgen', '-o', nc_path, cdl_path])


def check_for_cdl(filename, filepath):
    '''
    Check for a metadata .cdl file and return the path to the netCDF file generated

    :param str filename: Input filename from user
    :param str filepath: Generated path to file on server
    '''
    if os.path.splitext(filename)[-1] == '.cdl':
        nc_file = filename.replace('.cdl', '.nc')
        nc_path = os.path.join(os.path.dirname(filepath),
                               encode(nc_file))
        generate_dataset(nc_path, filepath)
        filepath = nc_path
    return filepath

def encode(s):
    return base64.b64encode(s.encode('utf-8')).decode('ascii')
