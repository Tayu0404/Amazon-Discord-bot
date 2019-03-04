FROM python:3.6-stretch

MAINTAINER tayu

RUN pip install \
	beautifulsoup4 \
	selenium \
	joblib \
	discord.py \
	schedule

RUN set -ex; \
	apt-get update; \
	\
	apt-get install -y --no-install-recommends wget; \
	wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz; \
	tar zxvf geckodriver*.tar.gz; \
	mv geckodriver /usr/local/bin/; \
	rm geckodriver*.tar.gz; \
	\
	apt-get install -y --no-install-recommends firefox-esr; \
	\
	rm -rf /var/lib/apt/lists/*; \
	\
	mkdir /python
