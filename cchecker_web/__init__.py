#!/usr/bin/env python
'''
Compliance Checker Web
~~~~~~~~~~~~~~~~~~~~~~

'''

from flask import Blueprint, request
from flask import current_app as app

from flask.ext.cache import Cache
from functools import wraps

# Cache type is specified by config.yml
cache = Cache(config={'CACHE_TYPE':'simple'})

cchecker_web = Blueprint('cchecker_web', __name__, static_url_path='', static_folder='static', template_folder='templates')


from cchecker_web.controller import show_index
from cchecker_web.upload import upload_dataset
from cchecker_web.api import show_job
