FROM 534479722520.dkr.ecr.us-east-1.amazonaws.com/core:20181213.0

MAINTAINER RPS <devops@rpsgroup.com>

USER root

# Install redis service
RUN yum install -y redis

# Add our daemons:
RUN mkdir -p /etc/service/ccweb-app /etc/service/ccweb-worker-01
COPY contrib/docker/runit/web.sh /etc/service/ccweb-app/run
COPY contrib/docker/runit/worker.sh /etc/service/ccweb-worker-01/run
RUN chmod +x /etc/service/ccweb-app/run /etc/service/ccweb-worker-01/run

# Startup Shell script:
COPY contrib/docker/my_init.d/run.sh /etc/run.sh

# Add our project
RUN mkdir /usr/lib/ccweb /var/run/datasets /var/log/ccweb
COPY cchecker_web /usr/lib/ccweb/cchecker_web
COPY .bowerrc Gruntfile.js Assets.json bower.json package.json requirements.txt\
     app.py setup.py worker.py /usr/lib/ccweb/
COPY contrib/config/config.yml /usr/lib/ccweb/

# User for installing requirements
RUN useradd -ms /bin/bash ccweb
RUN chown -R ccweb:ccweb /usr/lib/ccweb /var/run/datasets /var/log/ccweb
WORKDIR /usr/lib/ccweb

# Install python dependencies
RUN pip install -U pip
RUN pip install cython --no-compile
RUN pip install numpy
#RUN pip install cf-units==2.0.2
RUN pip --version && pip install -r requirements.txt

# Install nodejs/npm and friends:
RUN (curl -sL https://rpm.nodesource.com/setup_10.x | bash) && \
    yum -y install nodejs && \
    npm install -g grunt-cli yarn

# Install web dependencies
USER ccweb
RUN yarn install && \
    grunt

CMD ["/bin/bash", "/etc/run.sh"]
EXPOSE 3000
