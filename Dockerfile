FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY ./requirements.txt usr/src/app

RUN pip install -r requirements.txt

COPY . /usr/src/app