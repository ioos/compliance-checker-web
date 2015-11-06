#!/usr/bin/env python
'''
Compliance Checker Web
~~~~~~~~~~~~~~~~~~~~~~

'''

from flask import Flask, url_for, jsonify
from flask_environments import Environments
import os


app = Flask(__name__)
from cchecker_web.reverse_proxy import ReverseProxied
app.wsgi_app = ReverseProxied(app.wsgi_app)


env = Environments(app, default_env='COMMON')
env.from_yaml('config.yml')
if os.path.exists('config.local.yml'):
    env.from_yaml('config.local.yml')

if app.config['LOGGING'] == True:
    import logging
    logger = logging.getLogger('cchecker_web.app')
    logger.setLevel(logging.DEBUG)

    log_directory = app.config['LOG_FILE_PATH']
    log_filename = os.path.join(log_directory,app.config['LOG_FILE'])
    if not os.path.exists(os.path.dirname(log_filename)):
        os.makedirs(os.path.dirname(log_filename))
    file_handler = logging.FileHandler(log_filename, mode='a+')

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(process)d - %(name)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    #app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.info('Application Process Started')

from cchecker_web import cchecker_web
app.register_blueprint(cchecker_web, url_prefix='')

import redis
redis_pool = redis.ConnectionPool(host=app.config.get('REDIS_HOST'),
                                  port=app.config.get('REDIS_PORT'),
                                  db=app.config.get('REDIS_DB'))
app.redis = redis.Redis(connection_pool=redis_pool)
redis_connection = app.redis

# rq
from rq import Queue
app.queue = Queue('default', connection=app.redis)

@app.context_processor
def url_process():
    def url_root():
        return url_for('.show_root')
    return {'url_root': url_root}


from cchecker_web.utils import setup_uploads
setup_uploads(app)

from cchecker_web import cache, csrf, mail
cache.init_app(app, config=app.config['CACHE'])
csrf.init_app(app)
mail.init_app(app)

# The compliance checker needs to load all plugins at runtime
from compliance_checker.runner import CheckSuite
CheckSuite.load_all_available_checkers()

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
