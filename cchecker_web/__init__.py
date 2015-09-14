#!/usr/bin/env python
'''
Compliance Checker Web
~~~~~~~~~~~~~~~~~~~~~~

'''

from flask import Blueprint

cchecker_web = Blueprint('cchecker_web', __name__, static_url_path='', static_folder='static', template_folder='templates')


from views import show_index
from routes import upload_dataset

