#!/bin/bash
set -ex

: ${MAX_CONTENT_LENGTH:=16793600}
: ${LOGGING:=true}
: ${LOG_FILE_PATH:=/var/log/ccweb/}
: ${LOG_FILE:=cchecker_web.log}
: ${UPLOAD_FOLDER:=/var/run/datasets}
: ${REDIS_HOST:=redis}
: ${REDIS_PORT:=6379}
: ${REDIS_DB:=0}
: ${DEBUG:=false}

cat << EOF > /usr/lib/ccweb/config.yml
COMMON: &common
  MAX_CONTENT_LENGTH: ${MAX_CONTENT_LENGTH}
  LOGGING: ${LOGGING}
  LOG_FILE_PATH: ${LOG_FILE_PATH}
  LOG_FILE: ${LOG_FILE}
  HOST: localhost
  PORT: 3000
  DEBUG: True
  UPLOAD_FOLDER: /var/run/datasets
  REDIS_HOST: redis
  REDIS_PORT: 6379
  REDIS_DB: 0
  DEBUG: True

  CACHE:
    CACHE_TYPE: simple

  GOOGLE_ANALYTICS_ID: ${GOOGLE_ANALYTICS_ID}

DEVELOPMENT: &development
  <<: *common
  DEBUG: True

PRODUCTION: &production
  <<: *common
  DEBUG: ${DEBUG}
EOF

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

#exec /usr/bin/python \
exec /usr/bin/python3.6 \
         /usr/lib/ccweb/worker.py &

exec /usr/local/bin/gunicorn \
         --workers 2 \
         --bind 0.0.0.0:3000 \
         --chdir /usr/lib/ccweb \
         --log-syslog \
         app:app
