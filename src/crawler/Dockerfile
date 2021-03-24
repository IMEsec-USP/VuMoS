FROM python:3.7

COPY crawler/Pipfile crawler/Pipfile.lock crawler/scrapy.cfg /app/

WORKDIR /app

RUN pip install pipenv

RUN pipenv install --system --deploy

RUN apt-get update -y
RUN apt-get install postgresql-client -y

COPY commons /app/commons

RUN pip install -r commons/requirements.txt

COPY crawler/docker-entrypoint.sh /app/

COPY crawler/logging.yaml /app/

COPY crawler/main.py /app/

COPY crawler/hdb /app/hdb

ENTRYPOINT ["./docker-entrypoint.sh"]
