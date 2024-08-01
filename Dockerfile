FROM rockylinux:8

LABEL maintainer="RPS <devops@rpsgroup.com>"

USER root

# Install EPEL release
RUN dnf -y install epel-release && \
    dnf -y install --enablerepo=powertools dnf-plugins-core && \
    dnf config-manager --set-enabled powertools

# Install nodejs/npm and friends
RUN dnf -y module enable nodejs:16 && \
    dnf -y install nodejs npm && \
    npm install -g grunt-cli yarn

# Install container dependencies
RUN dnf -y install redis httpd
RUN dnf -y groupinstall "Development Tools"
RUN dnf -y install gcc gcc-c++ make cmake curl-devel libxml2-devel hdf5 hdf5-devel netcdf

RUN systemctl enable httpd.service

# Startup Shell script
COPY contrib/docker/my_init.d/run.sh /etc/run.sh

# Add our project
RUN mkdir /usr/lib/ccweb /var/run/datasets /var/log/ccweb

COPY cchecker_web /usr/lib/ccweb/cchecker_web
COPY Gruntfile.js Assets.json package.json postinstall.js requirements.txt \
     app.py setup.py worker.py /usr/lib/ccweb/
COPY contrib/config/config.yml /usr/lib/ccweb/

# User for installing requirements
RUN useradd -ms /bin/bash ccweb
RUN chown -R ccweb:ccweb /usr/lib/ccweb /var/run/datasets /var/log/ccweb
WORKDIR /usr/lib/ccweb

# Install Python 3.8, development tools, and dependencies
RUN dnf -y install python38 python38-devel python38-pip && \
    python3.8 -m pip install --upgrade pip && \
    python3.8 -m pip --version && \
    pip3.8 install wheel

# Install udunits2 and set UDUNITS2_XML_PATH
RUN dnf -y install udunits2-devel udunits2
ENV UDUNITS2_XML_PATH=/usr/share/udunits/udunits2.xml

# Install Python dependencies
RUN pip3.8 install -r requirements.txt

# Install local dependencies
USER ccweb
RUN yarn install && \
    grunt

USER root

# Add our daemons
RUN mkdir -p /etc/service/ccweb-app /etc/service/ccweb-worker-01
COPY contrib/docker/runit/web.sh /etc/service/ccweb-app/run
COPY contrib/docker/runit/worker.sh /etc/service/ccweb-worker-01/run
RUN chmod +x /etc/service/ccweb-app/run /etc/service/ccweb-worker-01/run

# Don't run as root user
USER ccweb

CMD ["/bin/bash", "/etc/run.sh"]
EXPOSE 3000
