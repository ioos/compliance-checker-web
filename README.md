IOOS Compliance Checker Web
===========================

The IOOS Compliance Checker's web front end companion.

### License

```
The MIT License (MIT)

Copyright (C) 2015 RPS ASA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


### Installation

#### Required Libraries:

 - hdf5
 - netcdf
 - openssl
 - libxml2
 - libxslt
 - nodejs
 - npm
 - libgeos
 

### Required Services:

 - redis

### Installation

1. Clone the repository
   ```
   git clone https://github.com/ioos/compliance-checker-web/
   ```

2. Install node and JS dependencies
   ```
   npm install
   bower install
   grunt
   ```

## Running

### The UI

The application has two components that need to run. app.py and worker.py. For development it is sufficient to run:

```
python app.py
```

For production, you can use whatever WSGI service you desire, I personally use gunicorn.

```
gunicorn -w 2 -b 0.0.0.0:3000 app:app
```

### The Worker

The worker listens for incoming jobs from the UI through a redis connection.
After the job is executed the resulting report is stored on redis for an hour.

To run the worker:

```
python worker.py
```

In production environments it's better to run a few workers.


## Running with Docker

1. Create a network to run on
   ```
   docker network create ccweb
   ```

2. Launch redis
   ```
   docker run --net ccweb -d --name redis redis:3.0.7-alpine
   ```

3. Launch this container
   ```
   docker run --net ccweb -d --name ccweb -p 3000:3000 ioos/compliance-checker-web
   ```

4. Visit the docker host on port 3000


### Docker Environment Configurations

The following are a list of useful configuration variables that can be
specified using an environment file or specifying environment variables when
launching the docker container.

- `MAX_CONTENT_LENGTH`: Maximum number of bytes allowed for upload. Default is 16793600 (16 MiB)
- `LOGGING`: Should the application log information
- `LOG_FILE_PATH`: Root directory where logging should write files
- `LOG_FILE`: The filename in the directory to write log files to.
- `UPLOAD_FOLDER`: The folder where uploaded contents should be written to. Defaults to `/var/run/datasets`
