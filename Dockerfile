FROM centos/python-38-centos7

LABEL maintainer="RPS <devops@rpsgroup.com>"

USER root

# Install nodejs/npm and friends:
RUN (curl -sL https://rpm.nodesource.com/setup_10.x | bash) && \
    yum -y install nodejs && \
    npm install -g grunt-cli yarn

# Install container dependencies:
RUN yum -y install epel-release && \
    yum -y update && \
    yum -y install redis

RUN yum -y groupinstall "Development Tools"

RUN yum update -y \
    && yum install -y httpd \
    && yum clean all

RUN systemctl enable httpd.service

# Startup Shell script:
COPY contrib/docker/my_init.d/run.sh /etc/run.sh

# Add our project
RUN mkdir /usr/lib/ccweb /var/run/datasets /var/log/ccweb

COPY cchecker_web /usr/lib/ccweb/cchecker_web
COPY Gruntfile.js Assets.json package.json requirements.txt\
     app.py setup.py worker.py /usr/lib/ccweb/
COPY contrib/config/config.yml /usr/lib/ccweb/

# User for installing requirements
RUN useradd -ms /bin/bash ccweb
RUN chown -R ccweb:ccweb /usr/lib/ccweb /var/run/datasets /var/log/ccweb
WORKDIR /usr/lib/ccweb

# Install python dependencies
RUN python3.8 -m pip install --upgrade pip &&\
    python3.8 -m pip --version &&\
    pip install -r requirements.txt

# Install local dependencies
RUN chown -R ccweb ~/.config
USER ccweb
RUN yarn install && \
    grunt

USER root

# Add our daemons:
RUN mkdir -p /etc/service/ccweb-app /etc/service/ccweb-worker-01
COPY contrib/docker/runit/web.sh /etc/service/ccweb-app/run
COPY contrib/docker/runit/worker.sh /etc/service/ccweb-worker-01/run
RUN chmod +x /etc/service/ccweb-app/run /etc/service/ccweb-worker-01/run

# Don't run as root user
USER ccweb

CMD ["/bin/bash", "/etc/run.sh"]
EXPOSE 3000
