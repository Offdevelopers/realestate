#! /bin/bash

NAME="dailynaijatv"
DIR=/home/avetiz/dailynaija/dailynaijatv/dailynaijatv
USER=avetiz
GROUP=avetiz
WORKERS=3
BIND=unix:/home/avetiz/dailynaija/bin/dailynaijatv/run/gunicorn.sock
DJANGO_SETTINGS_MODULE=dailynaijatv.settings
DJANGO_WSGI_MODULE=dailynaijatv.wsgi
LOG_LEVEL=error
TIMEOUT=300
cd $DIR
source ../../bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DIR:$PYTHONPATH

exec ../../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $WORKERS \
  --timeout $TIMEOUT\
  --user=$USER \
  --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=-
~
~

[program:avetiz]
command=/home/avetiz/dailynaija/bin/avetiz/gunicorn_start
user=avetiz
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/avetiz/dailynaija/bin/avetiz/logs/gunicorn-error.log
~
~



nginx conf

upstream app_servertwo {
    server unix:/home/avetiz/dailynaija/bin/avetiz/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80 default_server;

    # add here the ip address of your server
    # or a domain pointing to that ip (like example.com or www.example.com)
    server_name avetiz.com www.avetiz.com;

    keepalive_timeout 5;
    client_max_body_size 4G;

    access_log /home/avetiz/dailynaija/bin/avetiz/logs/nginx-access.log;
    error_log /home/avetiz/dailynaija/bin/avetiz/logs/nginx-error.log;
    location /static/ {
        alias /home/avetiz/dailynaija/realesate/static/;
    }

    # checks for static file, if not found proxy to app
    location / {
        try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header Host $http_host;
      proxy_redirect off;
      proxy_pass http://app_servertwo;
    }




}
