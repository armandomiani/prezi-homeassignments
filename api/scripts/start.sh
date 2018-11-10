#!/bin/bash

# listen attribute of nginx conf in order to set a port
# cheapers atrribute of uswgi in order to control the number of workers
#  which will process the requests

/usr/bin/envsubst '$API_PORT' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/nginx.conf
/usr/bin/envsubst '$WORKERS' < /etc/uwsgi/uwsgi.ini.template > /etc/uwsgi/uwsgi.ini
/usr/bin/supervisord
