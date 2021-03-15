FROM python:3.7

LABEL version="1.0.0"
LABEL mantainer="imesec@ime.usp.br"

RUN apt-get update
RUN apt-get install nmap -y
RUN apt-get install postgresql-client -y

RUN mkdir /home/nmap

WORKDIR /home/nmap

ENTRYPOINT ["./docker-entrypoint.sh"]
