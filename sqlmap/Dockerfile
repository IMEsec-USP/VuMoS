FROM python:3.7

COPY sqlmap/main.py sqlmap/requirements.txt /home/sqlmap/

WORKDIR /home/sqlmap

RUN apt-get update -y
RUN apt-get install postgresql-client -y
RUN apt-get install sqlmap -y

COPY commons /home/sqlmap/commons

RUN pip install -r commons/requirements.txt

COPY sqlmap/docker-entrypoint.sh ./

COPY sqlmap/src ./src

ENTRYPOINT ["./docker-entrypoint.sh"]