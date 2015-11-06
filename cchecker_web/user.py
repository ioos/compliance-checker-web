#!/usr/bin/env python
'''

'''

from flask import session, jsonify, request, current_app as app
from cchecker_web import cchecker_web as api
from cchecker_web import cache
from cchecker_web.email import send
from cchecker_web import valid_csrf
from uuid import uuid4
from userapp import UserAppServiceException
from datetime import datetime
import json
import redis
import re
import userapp
import hashlib

class UserError(IOError):
    pass

class MailError(IOError):
    pass

class TempUser(object):
    def __init__(self):
        self.redis = redis.StrictRedis()

    def create(self, options):
        user_id = options['login']
        options['user_id'] = user_id
        if self.exists(user_id):
            raise UserError("User account %s is already registered" % user_id)
        self.redis.set('user:%s' % user_id, json.dumps(options))
        return options

    def read(self, user_id):
        if user_id == 'self':
            user_id = session['user_id']
        data = self.redis.get('user:%s' % user_id)
        if data is None:
            raise UserError('No user account with that username exists')
        return json.loads(data)

    def update(self, options):
        user_id = options['user_id']
        data = json.loads(self.redis.get('user:%s' % user_id))
        data.update(options)
        self.redis.set('user:%s' % user_id, json.dumps(data))
        return data

    def delete(self, user_id):
        self.redis.delete('user:%s' % user_id)

    def exists(self, user_id):
        return self.redis.exists('user:%s' % user_id)

    def list(self):
        users = []
        for key in self.redis.keys('user:*'):
            user_id = re.sub(r'user:', '', key)
            users.append(self.read(user_id))
        return users

    def has_permission(self, user_id, permission):
        pass

    def login(self, user_id, password):
        user = self.read(user_id)
        if password == user['password']:
            token = uuid4().hex
            return {'user_id' : user_id, 'token' : token}
        raise UserError('Password incorrect')


class UserAppStore(object):
    user_option_keys = ['first_name', 'last_name', 'email', 'login']
    def __init__(self, token):
        self.api = userapp.API(app_id=app.config['USERAPP']['APPLICATION_ID'])
        if token is not None:
            self.api.set_option('token', token)

    def create(self, options):
        user = { key : options[key] for key in self.user_option_keys }
        user['password'] = options['password']

        response = self.api.user.save(**user)
        options['user_id'] = response['user_id']
        return options

    def read(self, user_id):
        response = self.api.user.get(user_id=user_id)
        user_dict = response[0]
        response = { key : user_dict[key] for key in self.user_option_keys }
        response['user_id'] = user_dict['user_id']
        return response

    def email_lookup(self, email):
        search_results = self.api.user.search(fields=['user_id', 'login', 'email'], page_size=100)
        search_results = serialize_userapp(search_results)
        for user in search_results['items']:
            if user['email'] == email:
                return user['user_id']
        else:
            raise UserError('No such user')

    def update(self, user_id, options):
        user = { key : options[key] for key in self.user_option_keys }
        user['user_id'] = user_id

        response = self.api.user.save(**user)
        return user

    def delete(self, user_id):
        count = self.api.user.remove(user_id=user_id)
        return {'count':count}

    def has_permission(self, user_id, permission):
        permissions = self.api.user.has_permission(user_id=user_id, permission=permission)
        if permission in permissions['missing_permissions']:
            return False
        return True

    def set_token(self, token):
        self.api.set_option('token', token)

    def list_users(self, page=1, page_size=20):
        fields = self.user_option_keys + ['user_id', 'permissions']
        response = self.api.user.search(page=page, page_size=page_size, fields=fields)
        users = serialize_userapp(response)
        for user in users['items']:
            user['permissions'] = [p for p in user['permissions'] if user['permissions'][p]['value'] is True]
        return users

    def login(self, login, password):
        response = self.api.user.login(login=login, password=password)
        token = response['token']
        user_id = response['user_id']

        user = self.api.user.get(user_id=user_id)
        if user:
            user = user[0]
        else:
            raise UserError('No such user')
        permissions = []
        for key, value in user['permissions'].source.iteritems():
            if value['value'] is True:
                permissions.append(key)
        return {
            'token' : token,
            'user_id' :user_id,
            'permissions' : permissions
        }

    def change_password(self, password_token, new_password):
        response = self.api.user.change_password(password_token=password_token, new_password=new_password)

    def reset_password(self, user_id):
        response = self.api.user.reset_password(user_id=user_id)
        return response



def serialize_userapp(o):
    if isinstance(o, userapp.IterableObject):
        return serialize_userapp(o.source)
    if isinstance(o, dict):
        return {k : serialize_userapp(v) for k,v in o.iteritems()}
    if isinstance(o, (list, tuple)):
        return [serialize_userapp(i) for i in o]
    return o




@api.route('/api/user', methods=['POST'])
@api.route('/api/user/', methods=['POST'])
@valid_csrf
def create_user():
    user_store = UserAppStore(None)
    data = json.loads(request.data)
    try:
        user_store.create(data)
    except (UserError,UserAppServiceException) as e:
        return jsonify(error="user_error", message=e.message), 400
    return jsonify(**data)


@api.route('/api/user/<string:user_id>', methods=['GET'])
def show_user(user_id):
    if 'user_id' not in session or 'user_token' not in session:
        return jsonify(error='unauthorized', message='You must be logged in and have privileges to view this user account'), 401
    try:
        user_token = session['user_token']
        user_store = UserAppStore(user_token)
        if user_store.has_permission('self', 'admin'):
            user_store.set_token(app.config['USERAPP']['API_KEY'])
        response = user_store.read(user_id)
    except (UserError,UserAppServiceException) as e:
        app.logger.error(e.message)
        return jsonify(error='user_error', message=e.message), 400
    return jsonify(**response)

@api.route('/api/user/<string:user_id>', methods=['PUT'])
@valid_csrf
def update_user(user_id):
    data = json.loads(request.data)
    if 'user_id' not in session or 'user_token' not in session:
        return jsonify(error='unauthorized', message='You do not have privileges to view this user account.'), 401
    try:
        user_token = session['user_token']
        user_store = UserAppStore(user_token)
        if user_store.has_permission('self', 'admin'):
            user_store.set_token(app.config['USERAPP']['API_KEY'])
        response = user_store.update(user_id, data)
    except (UserError,UserAppServiceException) as e:
        return jsonify(error='user_error', message=e.message), 400

    return jsonify(**response)

@api.route('/api/user', methods=['GET'])
@api.route('/api/user/', methods=['GET'])
def list_users():
    if 'user_id' not in session or 'user_token' not in session:
        return jsonify(error='unauthorized', message='You do not have privileges to view this user account.'), 401
    try:
        user_token = session['user_token']
        user_store = UserAppStore(user_token)
        if user_store.has_permission('self', 'admin'):
            user_store.set_token(app.config['USERAPP']['API_KEY'])
        else:
            return jsonify(error='unauthorized', message='You do not have privileges to view this user account.'), 401
        page = request.args.get('page', 1)
        response = user_store.list_users(page=page)
    except (UserError,UserAppServiceException) as e:
        return jsonify(error='user_error', message=e.message), 400

    return jsonify(**response)

@api.route('/api/user/login', methods=['POST'])
@valid_csrf
def login():
    data = json.loads(request.data)
    login = data['login']
    password = data['password']
    try:
        user_store = UserAppStore(None)
        data = user_store.login(login, password)
        session['user_token'] = data['token']
        session['user_id'] = data['user_id']
        session['permissions'] = data['permissions']
        return jsonify(**data)
    except (UserError,UserAppServiceException) as e:
        return jsonify(error='user_error', message=e.message), 400

@api.route('/api/user/logout', methods=['GET'])
def logout():
    if 'user_token' in session:
        del session['user_token']
        del session['user_id']
        del session['permissions']
        return jsonify(), 204
    return jsonify(error='user_error', message='Not currently logged in'), 400

@api.route('/api/user/change_password', methods=['POST'])
@valid_csrf
def change_password():
    data = json.loads(request.data)
    user_id = data['user_id']
    password = data['password']
    old_password = data['password_old']
    temporary_key = data['temporary_key']

    try:
        user_store = UserAppStore(app.config['USERAPP']['API_KEY'])
        response = user_store.change_password(password_token=old_password, new_password=password)
        app.redis.delete(temporary_key)
        user = user_store.read(user_id=user_id)
        login = user['login']
        data = user_store.login(login, password)
        session['user_token'] = data['token']
        session['user_id'] = data['user_id']
        session['permissions'] = data['permissions']
    except (UserError,UserAppServiceException) as e:
        return jsonify(error='user_error', message=e.message), 400
    except Exception as e:
        return jsonify(error='unknown', message=e.message), 400
    return jsonify(), 204

@api.route('/api/user/reset', methods=['POST'])
@valid_csrf
def reset_password():
    data = json.loads(request.data)
    email = data.get('email')
    try:
        send_password_reset_email(email)
    except (UserError,UserAppServiceException,MailError) as e:
        app.logger.exception(e.message)
        if isinstance(e, MailError):
            return jsonify(error='mail_error', message=e.message), 500
        return jsonify(error='user_error', message=e.message), 400
    return jsonify(message="Password Sent to email")

def send_password_reset_email(email):
    user_store = UserAppStore(app.config['USERAPP']['API_KEY'])
    user_id = user_store.email_lookup(email)
    password = user_store.reset_password(user_id)
    password = password['password_token']

    m = hashlib.sha224()
    message = '%s:%s:%s' % (email, app.config['SECRET_KEY'], datetime.utcnow().isoformat())
    m.update(message)
    key = m.hexdigest()

    reset_information = json.dumps({"password_token": password, "user_id": user_id})
    
    app.redis.set('user:reset:%s' % key, reset_information, 6400)

    url = request.url_root + 'user/reset_password/%s' % key
    message = '''
Please visit %s to reset your password.

Thank you!

- MyGLOS Team
'''
    
    try:
        send('Compliance Checker - Password Reset', [email], [], message % url, None)
    except Exception as e:
        app.logger.exception("Failed to send message")
        raise MailError("Failed to send message: %s" % e.message)

