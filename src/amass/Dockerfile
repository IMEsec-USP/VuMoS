FROM caffix/amass as build

LABEL version="1.0.0"
LABEL mantainer="imesec@ime.usp.br"

RUN mkdir /home/amass

RUN apk add --update python3 && \
	ln -sf python3 /usr/bin/python && \
	python3 -m ensurepip && \
	pip3 install --upgrade pip

RUN apk add postgresql-dev
RUN apk add postgresql-client

RUN apk add libc-dev && \
	apk add python3-dev && \
	apk add gcc

WORKDIR /home/amass

COPY amass/main.py amass/requirements.txt amass/docker-entrypoint.sh ./

RUN pip install -r requirements.txt

COPY amass/src ./src

COPY commons ./commons

RUN pip install -r commons/requirements.txt

ENTRYPOINT ["/home/amass/docker-entrypoint.sh"]
