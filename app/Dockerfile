FROM python:3.10-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install required packages
RUN apt-get update && apt-get install -y \
    nginx build-essential \
    python-dev \
    uwsgi-plugin-python3

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 80 443

# which uwsi .ini file to use
ENV UWSGI_INI /app.ini
# By default, run 2 processes
ENV UWSGI_CHEAPER 2
# By default, when on demand, run up to 16 processes
ENV UWSGI_PROCESSES 4

ENV NGINX_WORKER_PROCESSES 1
ENV LISTEN_PORT 80

RUN useradd -ms /bin/bash nginx

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./app.ini /app.ini
COPY ./app /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD nginx && \
    uwsgi --ini /app.ini --binary-path /usr/local/bin/uwsgi && \
    /bin/sh -c 'while :; do sleep 12h & wait $${!}; nginx -s reload; done & nginx -g \"daemon off;\"'
