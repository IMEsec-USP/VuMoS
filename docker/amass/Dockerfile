FROM caffix/amass as build

RUN apk add --update python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --upgrade pip

COPY commons amass/commons
COPY recon/amass amass

WORKDIR amass
 

ENTRYPOINT ["python3"]



