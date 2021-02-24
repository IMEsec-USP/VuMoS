FROM caffix/amass as build

RUN apk add --update python3 && \
	ln -sf python3 /usr/bin/python && \
	python3 -m ensurepip && \
	pip3 install --upgrade pip && \
	mkdir /home/amass

WORKDIR /home/amass

ENTRYPOINT ["/home/amass/docker-entrypoint.sh"]
# ENTRYPOINT ["python3", "main.py"]
# ENTRYPOINT ["cat", "docker-entrypoint.sh"]