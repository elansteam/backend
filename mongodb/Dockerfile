FROM mongo:latest

COPY generate-keyfile.sh /generate-keyfile.sh

RUN mkdir -p /opt/keyfile && \
    /bin/bash /generate-keyfile.sh

COPY mongod.conf /etc/mongod.conf

COPY init.sh /docker-entrypoint-initdb.d/init.sh

CMD ["mongod", "-f", "/etc/mongod.conf"]
