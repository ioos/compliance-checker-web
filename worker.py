#!/usr/bin/env python
'''
worker.py
'''

import os
import redis
from rq import Worker, Queue, Connection
from app import redis_connection

listen = ['default']

from compliance_checker.runner import CheckSuite

CheckSuite.load_all_available_checkers()


with Connection(redis_connection):
    worker = Worker(map(Queue, listen))
    worker.work()
