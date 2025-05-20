#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
worker.py
'''
from rq import Worker, Queue
from app import redis_connection
from compliance_checker.runner import CheckSuite

import logging


listen = ['default']


CheckSuite.load_all_available_checkers()


logging.basicConfig(level=logging.DEBUG)

# Build Queue objects bound to our Redis connection
queues = [Queue(name, connection=redis_connection) for name in listen]

worker = Worker(queues, connection=redis_connection)
worker.work()
