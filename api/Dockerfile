FROM python:3.5

MAINTAINER Armando Miani <armando.miani@gmail.com>

# install uwsgi
RUN pip install uwsgi bottle mongoengine pytest pytest-cov boddle

# install nginx and supervisor
RUN apt-get update && apt-get install -y nginx supervisor gettext-base

# remove default nginx configuration
RUN rm /etc/nginx/sites-available/default

# copy the configuration files
COPY conf/nginx.conf.template /etc/nginx/conf.d
COPY conf/uwsgi.ini.template /etc/uwsgi/
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY . /api
WORKDIR /api

RUN chmod +x -v /api/scripts/*.sh
RUN ln -s /api/scripts/run-tests.sh /usr/local/bin/run-tests.sh

CMD ["/api/scripts/start.sh"]
