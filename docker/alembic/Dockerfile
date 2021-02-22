FROM python:3.7

RUN python3 -m ensurepip && \ 
    pip3 install --upgrade pip && \
    mkdir /home/alembic && \

    #pip3 install -r ../requirements.txt && \
WORKDIR /home/alembic
ENTRYPOINT ["docker-entrypoint.sh"]


