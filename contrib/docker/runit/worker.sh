#!/bin/bash
exec /sbin/setuser ccweb \
     /opt/conda/bin/python \
         /usr/lib/ccweb/worker.py
