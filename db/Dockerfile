FROM postgres:latest

COPY *.sql /docker-entrypoint-initdb.d/
COPY backup.sh /backup.sh
RUN mkdir /backups
