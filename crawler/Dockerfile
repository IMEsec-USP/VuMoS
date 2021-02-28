FROM python:3.7

COPY hdb /app/hdb

WORKDIR /app

COPY Pipfile Pipfile.lock scrapy.cfg /app/

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD ["python", "-m", "scrapy", "crawl", "sqlsearch", "-o", "/dev/stdout:json"]