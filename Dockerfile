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

# Install Python 3.11 from source
RUN dnf -y install openssl-devel bzip2-devel libffi-devel sqlite-devel \
               zlib-devel readline-devel tk-devel xz-devel wget && \
    cd /usr/src && \
    wget https://www.python.org/ftp/python/3.11.6/Python-3.11.6.tgz && \
    tar xzf Python-3.11.6.tgz && \
    cd Python-3.11.6 && \
    ./configure --enable-optimizations --with-ensurepip=install && \
    make -j "$(nproc)" && \
    make altinstall && \
    # Symlink python3.11 / pip3.11 to python3 / pip3
    ln -sf /usr/local/bin/python3.11 /usr/bin/python3 && \
    ln -sf /usr/local/bin/pip3.11 /usr/bin/pip3 && \
    # Upgrade pip and install wheel
    python3 -m pip install --upgrade pip wheel && \
    # Clean up source
    cd / && rm -rf /usr/src/Python-3.11.6*


# Startup Shell script
COPY contrib/docker/my_init.d/run.sh /etc/run.sh


# Install Python dependencies (cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip install -r requirements.txt

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
