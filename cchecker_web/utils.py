#!/usr/bin/env
'''
Compliance Checker Web
~~~~~~~~~~~~~~~~~~~~~~

'''

import os

def setup_uploads(app):
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
