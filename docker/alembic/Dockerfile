FROM python:3.7

RUN python3 -m ensurepip && \
    pip3 install --upgrade pip && \
    mkdir /home/alembic

WORKDIR /home/alembic

ENTRYPOINT ["/home/alembic/docker-entrypoint.sh"]
