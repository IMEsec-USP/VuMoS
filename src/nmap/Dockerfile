FROM python:3.7

LABEL version="1.0.0"
LABEL mantainer="imesec@ime.usp.br"

RUN apt-get update
RUN apt-get install nmap -y
RUN apt-get install postgresql-client -y

RUN mkdir /home/nmap

WORKDIR /home/nmap

COPY nmap/main.py nmap/requirements.txt nmap/docker-entrypoint.sh ./

RUN pip install -r requirements.txt

COPY nmap/src ./src

COPY commons ./commons

RUN pip install -r commons/requirements.txt

ENTRYPOINT ["./docker-entrypoint.sh"]
