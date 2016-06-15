FROM phusion/baseimage:0.9.18

MAINTAINER Luke Campbell <luke.campbell@rpsgroup.com>

RUN apt-get update && apt-get install -y \
      git \
      libffi-dev \
      libhdf5-dev \
      libnetcdf-dev \
      netcdf-bin \
      libssl-dev \
      libxml2-dev \
      libxslt1-dev \
      nodejs \
      npm \
      python-dev \
      python-pip \
      libudunits2-0 \
      redis-tools \
      libgeos-dev \
      libpng12-dev \
      libfreetype6-dev \
      && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
# The debian version of six caused a bug in Flask
RUN pip install -U 'numpy==1.11.0' 'netCDF4==1.2.4'
RUN pip install -U six
RUN pip install cc-plugin-ncei
RUN pip install gunicorn supervisor

# install node dependencies and rename link node binary
RUN npm install -g bower grunt-cli && npm cache clear && \
    ln -s /usr/bin/nodejs /usr/bin/node

# Directory for the project
RUN mkdir /usr/lib/cchecker-web

# Copy over project contents
COPY cchecker_web /usr/lib/cchecker-web/cchecker_web
COPY .bowerrc app.py Gruntfile.js Assets.json bower.json package.json setup.py worker.py /usr/lib/cchecker-web/
COPY contrib/config/config.yml /usr/lib/cchecker-web/config.yml

RUN useradd -m web
RUN chown -R web:web /usr/lib/cchecker-web

# Install project dependencies
WORKDIR /usr/lib/cchecker-web
USER web

RUN npm install
RUN bower install
RUN grunt

USER root

# Set up container-wide services 
RUN mkdir /etc/supervisor/

COPY contrib/config/supervisord.conf /etc/supervisor/supervisord.conf
COPY contrib/docker/my_init.d /etc/my_init.d

# Logging and file support
RUN mkdir /var/log/ccweb
RUN mkdir /var/run/datasets

RUN chown -R web:web /var/log/ccweb
RUN chown -R web:web /var/run/datasets

EXPOSE 3000


CMD ["/sbin/my_init", "--", "/sbin/setuser", "web", "supervisord", "-c", "/etc/supervisor/supervisord.conf"]
