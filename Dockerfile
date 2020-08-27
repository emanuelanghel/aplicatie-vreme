FROM python:3.8-buster

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /the_weather
WORKDIR /the_weather
COPY ./the_weather /the_weather