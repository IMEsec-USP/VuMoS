FROM python:3.7

COPY sqlmap/main.py sqlmap/requirements.txt /app/

WORKDIR /sqlmap

RUN apt-get update -y
RUN apt-get install postgresql-client -y
RUN apt-get install sqlmap -y

COPY commons /sqlmap/commons

RUN pip install -r commons/requirements.txt

COPY sqlmap/docker-entrypoint.sh /sqlmap/

COPY sqlmap/src /sqlmap/hdb

ENTRYPOINT ["./docker-entrypoint.sh"]