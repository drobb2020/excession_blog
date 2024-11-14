# Deploying to an Ubuntu Server

IMPORTANT: When running these commands and configurations on the server make sure you are doing this as root. By default Ubuntu does not allow a direct login as root since the account does not have a password. To set a password on the root user do the following:

NOTICE: This document assumes that the project you wish to deploy to Ubuntu is fully functioning in a development environment.

- sudo passwd root
- enter the password you want to set for root
- repeat the password

Now log off the server and re-authenticate as root with the password you set and run the commands in this document.

## Preparing the Server

Install the following additional software packages on the server

* [X] python3-pip
* [X] python3-dev
* [X] python-dev-is-python3
* [X] pkg-config
* [X] libcariro2-dev
* [X] libpq-dev
* [X] postgresql
* [X] postgresql-contrib
* [X] nginx
* [X] supervisor

## Create a Local user & folder for the Django Project

Run the following command to create a folder to host the project:

* [X] ```mkdir -p /webapps/excession_blog```
* [X] Create a Linux group and user to own the project
  * [X] ```groupadd --system webapps```
  * [X] ```useradd -d /webapps/excession_blog blogadmin -g webapps -M -r -s /bin/bash```
  * [X] Set a password on blogadmin ```passwd blogadmin``` (Excess10n2411)
  * [X] Add blogadmin to sudoers group ```usermod -aG sudo blogadmin```

## Creating the Database

Run the following commands to create the postgresql database:

* [X] Login into the postgresql console: ```sudo -u postgres psql```
* [X] Run the following set of commands
  * [X] ```ALTER USER postgres with encrypted password 'Excess10n';```
  * [X] ```CREATE DATABASE excsblogdb;```
  * [X] ```CREATE USER excsblogadmin WITH PASSWORD 'excess10n2411';```
  * [X] ```ALTER ROLE excsblogadmin SET client_encoding TO 'utf8';```
  * [X] ```ALTER ROLE excsblogadmin SET default_transaction_isolation TO 'read committed';```
  * [X] ```ALTER ROLE excsblogadmin SET timezone TO 'UTC';```
  * [X] ```GRANT ALL PRIVILEGES ON DATABASE excsblogdb TO excsblogadmin;```
* [X] Verify database creation with command: ```\l```
* [X] \q to exit

## Creating a python virtual environment

Create a virtual environment for Python (as root)

* [X] Install virtualenv (or venv)
  * [X] python -m pip install --upgrade pip
  * [X] python -m pip install venv
* [X] Create environment
  * [X] cd /webapps/excession_blog
  * [X] python -m venv env_3.12.3
  * [X] source env_3.11.9/bin/activate
  * [X] cd env_3.12.3/

## Run a Pre Deployment Check

* [X] Run ```python manage.py check deploy```
* [X] Review the results in the console output
* [X] You should not have DEBUG set to True in production.
  * [X] Change the first line in the .env file (ENVIRONMENT) from development to production, this will change debug to False.
* [X] You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
  * [X] The change of the ENVIRONMENT setting in .env will set the CSRF_COOKIE_SECURE to True
* [X] SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
  * [X] The change of the ENVIRONMENT setting in .env will set the SESSION_COOKIE_SECURE to True
* [ ] Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
  * [ ] In settings.py add the line SECURE_SSL_REDIRECT = True
* [ ] You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
  * [ ] Add the following lines to settings.py to configure HSTS on the server
  * SECURE_HSTS_SECONDS = 86400
  * SECURE_HSTS_PRELOAD = True
  * SECURE_HSTS_INCLUDE_SUBDOMAINS = True
* [ ] Push any changes up to Git.

## Cloning the Project from Github

* [X] Make sure you are inside the virtual environment folder (env_3.12.3/)
* [X] git clone https://github.com/drobb2020/excession_blog.git
* [X] Install packages and postgresql driver
  * [X] pip install -r requirements.txt
  * [X] pip install psycopg2-binary ( or psycopg2 or possibly the latest version)

## Configure settings.py for new database

* [X] Configure settings.py to use postgresql database
  * [X] Copy the current settings.py to settingsDev.py
  * [X] Edit settings.py and do the following:
    * [X] Go to ALLOWED_HOSTS and add the dns name of the server
    * [X] Go to DATABASES and make the following modifications
      * change 'django.db.backends.sqlite3' to 'django.db.backends.postgresql_psycopg2'
      * set NAME to excsblogdb
      * set USER to excsblogadmin
      * set PASSWORD to excession246
      * set HOST to localhost
      * set PORT to 5432 or ''
    * [X] run python manage.py makemigrations
    * [X] run python manage.py migrate
    * [X] run python manage.py createsuperuser
    * [X] run python manage.py collectstatic

## Install and configure gunicorn

* [X] pip install gunicorn
* [X] in the bin folder of the virtual environment create a script named gunicorn_start and add the following lines:

    ``` sh
    #!/bin/bash

    NAME='excession_blog'
    DJANGODIR=/webapps/excession_blog/env_3.12.3/excession_blog/excs_blog_project
    SOCKFILE=/webapps/excession_blog/env_3.12.3/run/gunicorn.sock
    USER=django
    GROUP=webapps
    NUM_WORKERS=5
    DJANGO_SETTINGS_MODULE=excs_blog_project.settings
    DJANGO_WSGI_MODULE=excs_blog_project.wsgi
    TIMEOUT=120

    cd $DJANGODIR
    source ../env_3.12.3/bin/activate
    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    export PYTHONPATH=$DJANGODIR:$PYTHONPATH

    RUNDIR=$(dirname $SOCKFILE)
    test -d $RUNDIR || mkdir -p $RUNDIR

    exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --timeout $TIMEOUT \
    --user=$USER --group=$GROUP \
    --bind=unix:$SOCKFILE \
    --log-level=debug \
    --log-file=-
    ```

* [X] chmod +x bin/gunicorn_start
* [X] ./bin/gunicorn_start (to test) (troubleshoot if it does not start, stop it if it does start)
* [X] at this point all the files and folders under env_3.12.3 are owned by root:root. This needs to be modified so that all files and folder are owned by django:webapps. To do this run the following command:
  * [X] make sure you are in the env_3.12.3 folder
  * [X] chown -R django:webapps .

## Install and Configure Supervisor

* [X] Install and setup supervisor
  * [X] apt install supervisor
  * [X] cd /etc/supervisor/conf.d/
  * [X] Create the following configuration file excession_blog.conf

    ```sh
    [program:excession_blog]
    command = /webapps/excession_blog/env_3.12.3/bin/gunicorn_start
    user = django
    stdout_logfile = /webapps/excession_blog/env_3.12.3/logs/supervisor.log
    redirect_stderr = true
    environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
    ```

    * [X] create the logs folder under env_3.12.3/
    * [X] Run supervisorctl reread - this should read in the excession_blog.conf file.
    * [X] Run supervisorctl update
    * [X] Run supervisorctl status to see the running status of excession_blog

## Install and Configure nginx

* [X] Setup nginx
  * [X] cd /etc/nginx/sites-available/
  * [X] create a excession_blog.conf file with the following contents:

    ```sh
    upstream excession_blog_app_server {
        server unix:/webapps/excession_blog/env_3.12.3/run/gunicorn.sock fail_timeout=0;
    }

    server {
        listen 80;
        server_name excs-s5131.excession.org;

        access_log /webapps/excession_blog/env_3.12.3/logs/nginx-blog-access.log;
        error_log /webapps/excession_blog/env_3.12.3/logs/nginx-blog-error.log;

        location /static/ {
            alias /webapps/excession_blog/env_3.12.3/excession_blog/static/;
        }

        location /media/ {
            alias /webapps/excession_blog/env_3.12.3/excession_blog/media/;
        }

        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            proxy_set_header Host $http_host;

            proxy_redirect off;

            if (!-f $request_filename) {
                proxy_pass http://excession_blog_app_server
            }
        }
    }
    ```

  * [X] cd ../sites-enabled/
  * [X] ln -sf ../sites-available/djangoblog.conf .
  * [X] service nginx restart
  * [X] If everything is running as expected, go back into settingsprod.py and change DEBUG = True to False
  * [X] Restart supervisor with the command: supervisorctl restart excession_blog
    - Whenever you make a change to any files in the django project you must restart the supervisor for the changes to take effect.
