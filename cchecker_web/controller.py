#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
cchecker_web/controller.py
'''
from cchecker_web import cchecker_web as api
from flask import render_template, redirect, url_for, jsonify
from flask import current_app as app
from glob import glob
import json
import os

def dot_get(o, path):
    i = path.split('.', 1)
    if len(i) > 1:
        return dot_get(o[i[0]], i[1])
    return o[i[0]]

def load_assets(key, path):
    assets_json = 'Assets.json'
    with open(assets_json, 'r') as f:
        assets = json.loads(f.read())

    assets = dot_get(assets, key)
    files = []
    for filepath in assets[path]:
        if '*' not in filepath:
            files.append(filepath)
        else:
            for glob_path in glob(filepath):
                files.append(glob_path)
    # Strip off the beginning piece
    files = [f.replace('cchecker_web/static','') for f in files]
    return files

def load_javascripts(key, template_name):
    path = 'cchecker_web/static/js/compiled/%s.js' % template_name
    if app.config['DEBUG']:
        scripts_list = []
        for js_file in load_assets(key, path):
            js_file = url_for('.static', filename=js_file)
            script = '<script src="%s" type="text/javascript"></script>' % js_file
            scripts_list.append(script)
        scripts = '\n'.join(scripts_list)
        return scripts
    path = path.replace('cchecker_web/static', '')
    path = url_for('.static', filename=path)
    return '<script src="%s" type="text/javascript"></script>' % path

def load_css(key, template_name):
    path = 'cchecker_web/static/css/compiled/%s.css' % template_name
    if app.config['DEBUG']:
        scripts_list = []
        for css_file in load_assets(key, path):
            css_file = url_for('.static', filename=css_file)
            script = '<link href="%s" rel="stylesheet" type="text/css" />' % css_file
            scripts_list.append(script)
        scripts = '\n'.join(scripts_list)
        return scripts
    path = path.replace('cchecker_web/static', '')
    path = url_for('.static', filename=path)
    return '<link href="%s" rel="stylesheet" type="text/css" />' % path


@api.route('/')
def show_root():
    return redirect(url_for('.show_index'))

@api.route('/index.html')
def show_index():
    scripts = load_javascripts('main.js', 'index')
    css = load_css('main.css', 'index')
    return render_template('index.html', scripts=scripts, css=css)

@api.route('/report/<string:job_id>')
def show_report(job_id):
    scripts = load_javascripts('main.js', 'report')
    css = load_css('main.css', 'report')
    return render_template('report.html', scripts=scripts, css=css)

