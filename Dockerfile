FROM alpine:latest

USER root

RUN set -x && \
    apk update && \
    apk add openrc --no-cache && \
    apk --update add mysql && \
    apk --update add mysql-client && \
    apk --update add mysql-dev && \
    apk --update add postgresql && \
    apk --update add postgresql-dev && \
    apk --update add openjdk8 && \
    apk --update add gcc && \
    apk --update add musl-dev && \
    apk --update add python2 && \
    apk --update add python2-dev && \
    apk --update add py2-pip && \
    apk --update add git && \
    apk --update add bash && \
    apk --update add curl && \
    apk --update add tar && \
    apk --update add openssl && \
    openrc && \
    touch /run/openrc/softlevel && \
    /usr/bin/mysql_install_db --user=mysql && \
    /etc/init.d/mariadb start && \
    /usr/bin/mysqladmin -u root password 'root' && \
    /etc/init.d/postgresql start && \
    rc-update add postgresql && \
    rc-update add mariadb

CMD ["bash"]

