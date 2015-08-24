#!/usr/bin/env python
'''
Compliance Checker Web
~~~~~~~~~~~~~~~~~~~~~~

'''
from cchecker_web import cchecker_web
from flask import render_template

@cchecker_web.route('/')
@cchecker_web.route('/index.html')
def show_index():
    return render_template('index.html')

