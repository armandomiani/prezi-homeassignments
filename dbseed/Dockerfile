FROM mongo:latest

MAINTAINER Armando Miani <armando.miani@gmail.com>

ENV DB_HOST $DB_HOST

COPY seed.json seed.sh wait-for-it.sh bulk-mongo.js  /work/

RUN chmod +x /work/seed.sh
RUN chmod +x /work/wait-for-it.sh

ENTRYPOINT /bin/bash /work/wait-for-it.sh ${DB_HOST}:27017 -- /work/seed.sh
