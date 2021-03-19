FROM python:3.7

LABEL version="1.0.0"
LABEL mantainer="imesec@ime.usp.br"

RUN python3 -m ensurepip && \
    pip3 install --upgrade pip

RUN mkdir /home/alembic && \
	mkdir /home/alembic/alembic

RUN apt-get update -y
RUN apt-get install postgresql-client -y

WORKDIR /home/alembic

COPY alembic/alembic/env.py alembic/env.py
COPY alembic/alembic.ini ./alembic.ini

COPY alembic/requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY alembic/docker-entrypoint.sh ./docker-entrypoint.sh

COPY commons /home/commons

ENTRYPOINT ["./docker-entrypoint.sh"]
