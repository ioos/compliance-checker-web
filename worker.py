#!/usr/bin/env python
'''
worker.py
'''

import os
import redis
from rq import Worker, Queue, Connection
from app import redis_connection

listen = ['default']

with Connection(redis_connection):
    worker = Worker(map(Queue, listen))
    worker.work()
