#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
cchecker_web/controller.py
'''
from cchecker_web import cchecker_web as api
from cchecker_web import login_required
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
@login_required
def show_index():
    scripts = load_javascripts('main.js', 'index')
    css = load_css('main.css', 'index')
    return render_template('index.html', scripts=scripts, css=css)

@api.route('/report/<string:job_id>')
@login_required
def show_report(job_id):
    scripts = load_javascripts('main.js', 'report')
    css = load_css('main.css', 'report')
    return render_template('report.html', scripts=scripts, css=css)

@api.route('/user/new', methods=['GET'])
def new_user():
    scripts = load_javascripts('main.js', 'new_user')
    css = load_css('main.css', 'new_user')
    return render_template('new_user.html', scripts=scripts, css=css)

@api.route('/user/edit/<string:user_id>', methods=['GET'])
@login_required
def edit_user(user_id):
    scripts = load_javascripts('main.js', 'edit_user')
    css = load_css('main.css', 'edit_user')
    return render_template('edit_user.html', scripts=scripts, css=css)

@api.route('/user/login', methods=['GET'])
def user_login():
    scripts = load_javascripts('main.js', 'login')
    css = load_css('main.css', 'login')
    return render_template('login.html', scripts=scripts, css=css)

@api.route('/user/logout', methods=['GET'])
@login_required
def user_logout():
    scripts = load_javascripts('main.js', 'logout')
    css = load_css('main.css', 'logout')
    return render_template('logout.html', scripts=scripts, css=css)

@api.route('/user/', methods=['GET'])
@login_required
def show_users():
    scripts = load_javascripts('main.js', 'show_users')
    css = load_css('main.css', 'show_users')
    return render_template('show_users.html', scripts=scripts, css=css)

@api.route('/user/reset_password/<string:key>', methods=['GET'])
def show_reset_password(key):
    reset_information = app.redis.get('user:reset:%s' % key)
    reset_information = json.loads(reset_information)
    user_id = reset_information['user_id']
    password_token = reset_information['password_token']
    scripts = load_javascripts('main.js', 'reset_password')
    css = load_css('main.css', 'reset_password')
    return render_template('reset_password.html', scripts=scripts, css=css, temporary_key=key, user_id=user_id, password_token=password_token)


