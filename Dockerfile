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
	apt-get install -y --no-install-recommends \
		fonts-liberation \
		libappindicator3-1 \
		libasound2 \
		libatk-bridge2.0-0 \
		libgtk-3-0 \
		libnspr4 \
		libnss3 \
		libx11-xcb1 \
		libxtst6 \
		lsb-release \
		xdg-utils\
		libgconf2-4 \
		libnss3-dev \
		wget \
		unzip; \
	\
	wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; \
	dpkg -i google-chrome*.deb; \
	rm google-chrome*.deb; \
	\
	wget https://chromedriver.storage.googleapis.com/2.43/chromedriver_linux64.zip; \
	unzip chromedriver_linux64.zip; \
	rm chromedriver_linux64.zip; \
	mkdir /python; \
	mv chromedriver /python/; \
	\
	#rm -rf /var/lib/apt/lists/*
