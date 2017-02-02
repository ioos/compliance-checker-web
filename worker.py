#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
worker.py
'''
from rq import Worker, Queue, Connection
from app import redis_connection
from compliance_checker.runner import CheckSuite

import logging


listen = ['default']


CheckSuite.load_all_available_checkers()


logging.basicConfig(level=logging.DEBUG)


with Connection(redis_connection):
    worker = Worker(map(Queue, listen))
    worker.work()
