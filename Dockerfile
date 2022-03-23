FROM python:3.9

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get update \
    && apt-get install -yyq netcat

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /backend
WORKDIR /backend

COPY ./requirements.txt /backend/
RUN pip install -r requirements.txt

COPY . /backend/


ENTRYPOINT ["./entrypoint.sh"]
