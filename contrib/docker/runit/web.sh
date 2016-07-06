#!/bin/bash
exec /sbin/setuser ccweb \
     /opt/conda/bin/gunicorn \
         --workers 2 \
         --bind 0.0.0.0:3000 \
         --chdir /usr/lib/ccweb \
         --log-syslog \
         app:app
