FROM python:3.7

LABEL version="1.0.0"
LABEL mantainer="imesec@ime.usp.br"

RUN python3 -m ensurepip && \
    pip3 install --upgrade pip && \
    mkdir /home/alembic

RUN apt-get update -y
RUN apt-get install postgresql-client -y

WORKDIR /home/alembic

ENTRYPOINT ["./docker-entrypoint.sh"]
