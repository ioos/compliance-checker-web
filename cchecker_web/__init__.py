#!/usr/bin/env python
'''
Compliance Checker Web
~~~~~~~~~~~~~~~~~~~~~~

'''

from flask import Blueprint

cchecker_web = Blueprint('cchecker_web', __name__, static_url_path='', static_folder='static', template_folder='templates')


from cchecker_web.controller import show_index
from cchecker_web.routes import upload_dataset
from cchecker_web.api import show_job
