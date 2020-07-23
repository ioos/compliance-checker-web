#!/bin/bash

set -e
wait_for_redis(){
    echo "Waiting for redis"
    until $(redis-cli -h redis ping > /dev/null 2>&1); do 
        printf '.'
        sleep 5
    done
    printf '\n'
}

wait_for_redis

exec /usr/bin/python \
         /usr/lib/ccweb/worker.py &

exec /usr/local/bin/gunicorn \
         --workers 2 \
         --bind 0.0.0.0:3000 \
         --chdir /usr/lib/ccweb \
         --log-syslog \
         app:app
