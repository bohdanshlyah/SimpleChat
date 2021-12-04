FROM python:3.9.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2-binary

COPY ./requirements.txt /requirements.txt
RUN pip install -r ./requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app