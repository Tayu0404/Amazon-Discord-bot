FROM python:3.6-stretch

MAINTAINER tayu

RUN pip install \
	beautifulsoup4 \
	selenium \
	joblib \
	discord.py \
	schedule

RUN apt-get update
RUN apt-get install -y\
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
	unzip

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome*.deb

RUN mkdir /python
